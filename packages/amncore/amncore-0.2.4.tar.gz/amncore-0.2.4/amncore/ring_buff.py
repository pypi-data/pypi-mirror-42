import bombfuse
import kthread
import select
import time
import threading

class RingStream(object):
    def __init__(self, ring):
        self.ring = ring
        self.seq = ring.base_sequence
        self.buff = ''
        
    def read(self, length = None):
        if length is not None and len(self.buff) >= length:
            data = self.buff[0:length]
            self.buff = self.buff[len(data):]
            return data
            
        while True:
            lseq, data = self.ring.read_data(self.seq)
            if lseq is None:
                return
                
            self.seq = lseq
            self.buff += data
            if length is not None:
                if len(self.buff) >= length:
                    retval = self.buff[0:length]
                    self.buff = self.buff[len(retval):]
                    return retval
                else:
                    time.sleep(0.25)
                    continue
                    
            data = self.buff
            self.buff = ''
            
            return data
            
            break
            
    def write(self, data):
        return self.ring.write(data)

class RingBuffer(object):
    def __init__(self, sock, **kwargs):
        if 'size' in kwargs:
            self.size = kwargs['size']
        else:
            self.size = (1024 * 4)
            
        self.fd = sock
        self.seq = 0
        self.beg = 0
        self.cur = 0
        self.queue = [None] * self.size
        self.mutex = threading.Lock()
        self.monitor = None
        self.monitor_thread_error = None
        
    def __repr__(self):
        current = super(RingBuffer, self).__repr__()[:-1]
        try:
            return current + ": size={} fd={} seq={} beg={} cur={}>".format(self.size, self.fd.fileno(), self.seq, self.beg, self.cur)
        except Exception:
            return current + ": size={} fd={} seq={} beg={} cur={}>".format(self.size, self.fd, self.seq, self.beg, self.cur)
        
    def start_monitor(self):
        if self.monitor is None:
            self.monitor = self.monitor_thread()
        
    def stop_monitor(self):
        if self.monitor is not None:
            self.monitor.kill()
            
        self.monitor = None
        
    def monitor_thread(self):
        thred = kthread.KThread(target = self.monitor_thread_func)
        thred.daemon = True
        thred.start()
        return thred
        
    def monitor_thread_func(self):
        try:
            while self.fd is not None:
                buff = self.fd.get_once(-1, 1.0)
                if buff is None:
                    continue
                self.store_data(buff)
        except Exception as e:
            self.monitor_thread_error = e
            
    def put(self, data, **kwargs):
        return self.fd.put(data, **kwargs)
        
    def clear_data(self):
        with self.mutex:
            self.seq = 0
            self.beg = 0
            self.cur = 0
            self.queue = [None] * self.size
            
    def store_data(self, data):
        with self.mutex:
            loc = 0
            if self.seq > 0:
                loc = (self.cur + 1) % self.size
                
                if loc <= self.beg:
                    self.beg = (self.beg + 1) % self.size
            
            self.queue[loc] = [self.seq + 1, data]
            self.seq += 1
            self.cur = loc
            
    def read_data(self, ptr = None):
        with self.mutex:
            if self.queue[self.beg] is None:
                return [None, None]
            else:
                if ptr is None:
                    ptr = self.queue[self.beg][0]

            if ptr is None:
                return [None, None]
                
            if ptr < self.queue[self.beg][0]:
                ptr = self.queue[self.beg][0]
                
            dis = self.seq - ptr
            
            if dis < 0:
                return [None, None]
                
            off = ptr - self.queue[self.beg][0]
            sett = (self.beg + off) % self.size
            
            buff = ""
            cnt = 0
            lst = ptr
            for i in range(ptr, self.seq + 1):
                block = self.queue[(sett + cnt) % self.size]
                lst, data = block[0], block[1]
                buff += data
                cnt += 1
                
            return [lst + 1, buff]
            
    @property
    def base_sequence(self):
        with self.mutex:
            if self.queue[self.beg] is None:
                return 0
            return self.queue[self.beg][0]
            
    @property
    def last_sequence(self):
        return self.seq
        
    def create_stream(self):
        return RingStream(self)
        
    def poll(self):
        return select.select([self.fd], [], [self.fd], 0.10)
        
    def wait(self, seq):
        nseq = None
        while nseq is None:
            nseq, data = self.read_data(seq)
            self.poll()
    
    def wait_for(self, seq, timeout = 1):
        try:
            bombfuse.timeout(timeout, self.wait, seq)
        except bombfuse.TimeoutError:
            pass
            
