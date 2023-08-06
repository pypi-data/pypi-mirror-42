import bombfuse
import errno
import kthread
try:
    import logger
except ImportError:
    from . import logger
import Queue
import select
import socket
import struct
try:
    import sync
except ImportError:
    from . import sync
import threading
import time
try:
    import xcepts
except ImportError:
    from . import xcepts

LogSource = "amncore"

class StreamMixin(object):
    def __init__(self, *args, **kwargs):
        """
        This class provides read/write functions that abstract an underlying stream
        """
        if 'sock' in kwargs and hasattr(self, "sock") == False:
            self.sock = kwargs['sock']
        else:
            self.sock = None

        if 'sslsock' in kwargs and hasattr(self, "sslsock") == False:
            self.sslsock = kwargs['sslsock']
        else:
            self.sslsock = None
            
    def write(self, buf, **kwargs):
        """
        Writes a supplied buffer to the underlying stream
        """
        total_sent = 0
        total_length = len(buf)
        block_size = 32768

        while (total_sent < total_length):
            try:
                s = sync.select_s([], [self.fd], [], 0.2)
                if (s == ([],[],[]) or len(s[1]) == 0):
                    continue

                data = buf[total_sent:total_sent + block_size]
                self.fd.setblocking(0)
                sent = self.fd.send(data)
                if sent > 0:
                    total_sent += sent
            except socket.error as e:
                if e.errno == errno.EAGAIN or e.errno == errno.EWOULDBLOCK:
                    # wait for 0.5 seconds, decrement block_size, retry
                    sync.select_s([], [self.fd], [], 0.5)
                    block_size = 1024
                    continue
                elif e.errno == errno.EPIPE:
                    return None
                return None
            except IOError as e:
                return None

        return total_sent
        
    def read(self, length = None, **kwargs):
        """
        Reads a buffer of supplied length from the underlying stream
        """
        while True:
            try:
                self.fd.setblocking(0)
                return self.fd.recv(length)
            except socket.error as e:
                if e.errno == errno.EAGAIN or e.errno == errno.EWOULDBLOCK:
                    sync.select_s([self.fd], [], [], 0.5)
                    continue
                elif e.errno == errno.EPIPE:
                    return None
            except IOError as e:
                return None
            except Exception as e:
                return None

    def has_read_data(self, timeout = None):
        """
        Polls the underlying stream (with an optional timeout) for read data.  Returns True is data is available, False otherwise
        """
        if timeout is not None and timeout == 0:
            timeout = 3600

        try:
            rv = select.select([self.fd], [], [], timeout)
            if ((rv is not None) and (rv != ([], [], [])) and (len(rv[0]) > 0) and (rv[0][0] == self.fd)):
                return True
            else:
                return False
        except socket.error as e:
            if (e.errno == errno.EBADF) or (e.errno == errno.ENOTSOCK):
                raise EOFError
            return False
        except (xcepts.StreamClosedError, IOError, EOFError) as e:
            return False
    
    @property
    def fd(self):
        """
        Returns an object passable to select.select() for polling
        """
        if hasattr(self, "fileno") == False:
            if hasattr(self, "sock") == True:
                return self.sock
            else:
                return None
        return self

    def timed_write(self, buf, wait = 10, **kwargs):
        """
        Attempts to write to the stream, optionally timing out after a provided value
        """
        if (wait is not None and wait > 0):
            return bombfuse.timeout(wait, self.write, buf, **kwargs)
        else:
            return self.write(buf, **kwargs)
            
    def timed_read(self, length = None, wait = 10, **kwargs):
        """
        Attempts to read from the stream, optionally timing out after a provided value
        """
        if (wait is not None and wait > 0):
            return bombfuse.timeout(wait, self.read, length, **kwargs)
        else:
            return self.read(length, **kwargs)
            
    def put(self, buf, **kwargs):
        """
        Writes an entire buffer to the underlying stream
        
        Args:
            buf (str): Buffer to write to the stream.
            Timeout (int): Number of seconds before the function times out.  Default: 0 (no timeout)
        """
        if (buf is None or len(buf) == 0):
            return 0
            
        send_len = len(buf)
        send_idx = 0
        if 'Timeout' in kwargs:
            wait = kwargs['Timeout']
        else:
            wait = 0
            
        while (send_idx < send_len):
            curr_len = self.timed_write(buf[send_idx:send_idx + (len(buf) - send_idx)], wait, **kwargs)
            
            if curr_len is None:
                return (len(buf) - send_len)
                
            send_len -= curr_len
            send_idx += curr_len
            
        return (len(buf) - send_len)

    def get_once(self, length = -1, timeout = 10):
        if (self.has_read_data(timeout) == False):
            return None
            
        if length == -1:
            bsize = 16384
        else:
            bsize = length
            
        data = self.read(bsize)
        # we got nothing
        if data is None or (len(data) == 0 and bsize != 0):
            raise EOFError("get_once() received no data")
            
        return data

    def get(self, timeout = None, ltimeout = 0.1, **kwargs):
        if timeout is not None and int(timeout) < 0:
            timeout = None
            
        # no read data available, quit
        if (self.has_read_data(timeout) == False):
            return None
            
        buf = ""
        lps = 0
        eof = False
        
        while (self.has_read_data(ltimeout) == True):
            try:
                temp = self.read(16384)
            except EOFError:
                # catch any EOF errors, gracefully exit
                eof = True
                
            if temp is not None and len(temp) == 0:
                # no more data is available, gracefully exit
                eof = True
                
            if eof == True:
                if len(buf) > 0:
                    break
                else:
                    # no data was ever read! raise an error
                    raise EOFError("get() received no data")
                
            if temp is None or len(temp) == 0:
                break
                
            buf += temp
            lps += 1
            
            if (lps >= 1024):
                break
                
        return buf

class StreamServerMixin(object):
    def __init__(self, *args, **kwargs):
        """
        This mixin provides underlying functions for server monitoring and client handling
        """
        if 'sock' in kwargs and hasattr(self, "sock") == False:
            self.sock = kwargs['sock']
        else:
            self.sock = None

        if 'sslsock' in kwargs and hasattr(self, "sslsock") == False:
            self.sslsock = kwargs['sslsock']
        else:
            self.sslsock = None

        self.client_waiter = None
        self.clients = []
        self.clients_thread = None
        self.listener_thread = None
        self.on_client_close_proc = None
        self.on_client_connect_proc = None
        self.on_client_data_proc = None
        
    def on_client_connect(self, client):
        """
        Callback method for handling incoming client connections
        """
        try:
            if self.on_client_connect_proc is not None:
                return self.on_client_connect_proc(client)
        except AttributeError:
            pass
            
    def on_client_data(self, client):
        """
        Callback method for handling incoming client data
        """
        try:
            if self.on_client_data_proc is not None:
                return self.on_client_data_proc(client)
        except AttributeError:
            pass
            
    def on_client_close(self, client):
        """
        Callback method for handling closed client connections
        """
        try:
            if self.on_client_close_proc is not None:
                return self.on_client_close_proc(client)
        except AttributeError:
            pass
            
    def start(self):
        """
        Starts the server monitor and client management threads
        """
        self.clients = []
        self.client_waiter = Queue.Queue()

        # use wait() to prevent threads from closing
        self.listener_thread = kthread.KThread(target=self.monitor_listener, name="StreamServerListener")
        self.listener_thread.daemon = True
        self.listener_thread.start()
        
        self.clients_thread = kthread.KThread(target=self.monitor_clients, name="StreamServerClientMonitor")
        self.clients_thread.daemon = True
        self.clients_thread.start()
        
    def stop(self):
        """
        Stops the server monitor and closes all client connections
        """
        try:
            self.listener_thread.terminate()
        except threading.ThreadError:
            pass

        try:
            self.clients_thread.terminate()
        except threading.ThreadError:
            pass
        
        for cli in self.clients:
            self.close_client(cli)
            
        del self.clients[:]

    def close_client(self, client):
        """
        Closes a client connection and removes it from the instance
        """
        if client is not None:
            try:
                self.clients.remove(client)
            except Exception as e:
                pass

            try:
                client.close()
            except IOError as e:
                pass
                
    def wait(self):
        """
        Halts the program until the server listener thread terminates
        """
        if self.listener_thread is not None:
            self.listener_thread.join()

    def monitor_listener(self):
        """
        Thread function that listens for and processes incoming connections to the server
        """
        while True:
            try:
                cli = self.accept()
            
                if cli is None:
                    # nonblock accept returned None
                    logger.ilog("The accept() function returned None in stream server listener monitor: {}".format(self), LogSource, logger.LEV_3)
                    time.sleep(0.50)
                    continue

                # got one, add it to the list
                self.clients.append(cli)
                # handle on-connection shit
                self.on_client_connect(cli)
                # pass cli to data monitor thread
                self.client_waiter.put(cli)

            except (IOError, EOFError) as e:
                if type(e) == IOError and e.errno == errno.EWOULDBLOCK:
                    time.sleep(0.50)
                pass
            except KeyboardInterrupt as e:
                raise e
            except Exception as e:
                logger.elog("Error in stream server listener monitor: {} {}".format(str(e), type(e)), LogSource, logger.LEV_1)
                logger.rlog(logger.ExceptionCallStack, LogSource, logger.LEV_1)
                break

    def monitor_clients(self):
        """
        Thread function that waits for and handles incoming client data
        """
        while True:
            try:
                if len(self.clients) == 0:
                    try:
                        self.client_waiter.get(False)
                    except Queue.Empty as e:
                        # no clients in queue
                        time.sleep(0.50)
                        continue

                # no clients available, keep waiting
                if len(self.clients) == 0:
                    time.sleep(0.50)
                    continue
                
                # poll for read data
                sd = sync.select_s(self.clients, [], [], None)
                
                # got something
                for cfd in sd[0]:
                    try:
                        # send to handler function
                        self.on_client_data(cfd)
                    except (EOFError, IOError) as e:
                        self.on_client_close(cfd)
                        self.close_client(cfd)
                    except KeyboardInterrupt as e:
                        raise e
                    except Exception as e:
                        self.close_client(cfd)
                        logger.elog("Error in stream server client monitor: {} {}".format(str(e), type(e)), LogSource, logger.LEV_1)
                        logger.rlog(logger.ExceptionCallStack, LogSource, logger.LEV_1)
            except Queue.Empty as e:
                time.sleep(0.20)
                continue
            except xcepts.StreamClosedError as e:
                self.clients.remove(e.stream)
            except KeyboardInterrupt as e:
                raise e
            except Exception as e:
                self.close_client(cfd)
                logger.elog("Error in stream server client monitor: {} {}".format(str(e), type(e)), LogSource, logger.LEV_1)
                logger.rlog(logger.ExceptionCallStack, LogSource, logger.LEV_1)
