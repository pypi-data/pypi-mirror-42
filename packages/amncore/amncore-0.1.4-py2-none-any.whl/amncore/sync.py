import select

try:
    import thread
except ImportError:
    import _thread as thread
    
import xcepts

DefaultCycle = 0.2

def select_s(rfd = [], wfd = [], efd = [], t = None):
    left = t
    
    if rfd is not None and len(rfd) > 0:
        for fd in rfd:
            try:
                if fd.fileno() == -1:
                    raise xcepts.StreamClosedError(fd)
            except Exception as e:
                raise xcepts.StreamClosedError(fd)

    while ((left is None) or (left > 0)):
        if rfd is not None and len(rfd) > 0:
            orig_size = len(rfd)
        try:
            rv = select.select(rfd, wfd, efd, DefaultCycle)
        except IOError as e:
            if rfd is not None and len(rfd) > 0:
                for fd in rfd:
                    try:
                        if fd.fileno() == -1:
                            raise xcepts.StreamClosedError(fd)
                    except Exception as e:
                        raise xcepts.StreamClosedError(fd)
                
            if (rfd is not None and len(rfd) != orig_size):
                return None

            raise e

        if (rv is not None):
            return rv

        if left is not None:
            left -= DefaultCycle

    return None

class Event(object):
    Infinite = 10000

    def __init__(self, state = False, auto_reset = True, param = None):
        self.state = state
        self.auto_reset = auto_reset
        self.param = param
        self.mutex = threading.Lock()
        self.cond = threading.Condition(self.mutex)

    def set(self, param = None):
        self.param = param
        with self.mutex:
            if (self.auto_reset == False):
                self.state = True
            self.cond.notify_all()

    def reset(self):
        self.param = None
        self.state = False

    def notify(self, param = None):
        self.set(param)

    def wait(self, t = Infinite):
        with self.mutex:
            if (self.state == True):
                return
            self.cond.wait(float(t))


class RefCount(object):
    def __init__(self, *args, **kwargs):
        self._references = 1
        self._references_mutex = threading.Lock()
        return self

    def ref(self):
        with self._references_mutex:
            self._references += 1
        return self

    def deref(self):
        retval = False
        with self._references_mutex:
            self._references -= 1
            if (self._references == 0):
                self.cleanup()
                retval = True
            else:
                retval = False
        return retval

    def cleanup(self):
        pass
        
class ReadWriteLock(object):
    def __init__(self):
        self.read_sync_mutex = threading.Lock()
        self.write_sync_mutex = threading.Lock()
        self.exclusive_mutex = threading.Lock()
        self.readers = 0
        self.writer = False
        self.owner = None
        
    def lock_read(self):
        self.read_sync_mutex.acquire()
        try:
            if (self.readers > 0) and (self.writer == True):
                self.read_sync_mutex.release()
                self.exclusive_mutex.acquire()
                self.exclusive_mutex.release()
                self.read_sync_mutex.acquire()
                
            self.readers = self.readers + 1
            
            if (self.readers == 1):
                self.exclusive_mutex.acquire()
                self.owner = thread.get_ident()
        finally:
            self.read_sync_mutex.release()
            
    def unlock_read(self):
        self.read_sync_mutex.acquire()
        try:
            unlocked = False
            while (unlocked == False):
                if (self.readers - 1 == 0):
                    if (self.owner is not None) and (thread.get_ident() == self.owner):
                        self.owner = None
                        self.exclusive_mutex.release()
                elif (self.owner is not None) and (thread.get_ident() == self.owner):
                    self.read_sync_mutex.release()
                    continue
                    
                unlocked = True
                self.readers = self.readers - 1
                
        finally:
            self.read_sync_mutex.release()
            
    def lock_write(self):
        self.write_sync_mutex.acquire()
        
        try:
            self.writer = True
            self.exclusive_mutex.acquire()
            self.owner = thread.get_ident()
        finally:
            self.write_sync_mutex.release()
            
    def unlock_write(self):
        if self.owner is not None and thread.get_ident() != self.owner:
            raise RuntimeError("Non-owner calling thread attempted to release write lock")
        
        self.writer = False
        
        self.exclusive_mutex.release()
    
    def synchronize_read(self, func = None, *args):
        self.lock_read()
        try:
            if func is not None:
                func(*args)
        finally:
            self.unlock_read()
            
    def synchronize_write(self, func = None, *args):
        self.lock_write()
        try:
            if func is not None:
                func(*args)
        finally:
            self.unlock_write()
            
    