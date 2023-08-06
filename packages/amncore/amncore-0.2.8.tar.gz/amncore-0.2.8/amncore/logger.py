import inspect
import re
import sys
import threading
import time
import traceback

LOG_ERROR = 'error'
LOG_DEBUG = 'debug'
LOG_INFO  = 'info'
LOG_WARN  = 'warn'
LOG_RAW   = 'raw'

LEV_0 = 0
LEV_1 = 1
LEV_2 = 2
LEV_3 = 3

class LogSink(object):
    def __init__(self, *args, **kwargs):
        pass

    def cleanup(self):
        pass

    def log(self, sev, src, level, msg):
        raise NotImplementedError

    def get_current_timestamp(self):
        return time.strftime("%m/%d/%Y %H:%M:%S", time.gmtime())

class FlatFileSink(LogSink):
    def __init__(self, file):
        self.fd = open(file, 'a')
        super(FlatFileSink, self).__init__()

    def cleanup(self):
        self.fd.close()

    def log(self, sev, src, level, msg):
        if sev == LOG_RAW:
            self.fd.write(msg)
        else:
            code = 'i'
            if sev == LOG_DEBUG:
                code = 'd'
            elif sev == LOG_ERROR:
                code = 'e'
            elif sev == LOG_INFO:
                code = 'i'
            elif sev == LOG_WARN:
                code = 'w'

            self.fd.write("[{}] [{}({})] {}: {}\n".format(self.get_current_timestamp(), code, level, src, msg))
        self.fd.flush()

class TimestampFlatFileSink(FlatFileSink):
    def __init__(self, file):
        super(TimestampFlatFileSink, self).__init__(file)

    def log(self, sev, src, level, msg):
        if msg is None or len(msg) == 0 or len(str(msg).strip()) == 0:
            return

        msg = re.sub(r'\x1b\[[0-9;]*[mG]', '', msg)
        msg = re.sub(r'[\x01-\x02]', ' ', msg)
        msg = re.sub(r'\s+$', msg)
        self.fd.write("[{}] {}\n".format(self.get_current_timestamp(), msg))
        self.fd.flush()

class StderrSink(LogSink):
    def __init__(self, *args, **kwargs):
        return super(StderrSink, self).__init__(*args, **kwargs)

    def log(self, sev, src, level, msg):
        if sev == LOG_RAW:
            sys.stderr.write(msg)
        else:
            code = 'i'
            if sev == LOG_DEBUG:
                code = 'd'
            elif sev == LOG_ERROR:
                code = 'e'
            elif sev == LOG_INFO:
                code = 'i'
            elif sev == LOG_WARN:
                code = 'w'

            sys.stderr.write("[{}] [{}({})] {}: {}\n".format(self.get_current_timestamp(), code, level, src, msg))
        sys.stderr.flush()

class LogDispatcher(object):
    def __init__(self, *args, **kwargs):
        self.log_sinks = {}
        self.log_levels = {}
        self.log_sinks_lock = threading.Lock()

    def __getitem__(self, src):
        sink = None

        with self.log_sinks_lock:
            if src in self.log_sinks:
                sink = self.log_sinks[src]
            else:
                sink = None

        return sink

    def __setitem__(self, src, sink):
        self.store(src, sink)

    def store(self, src, sink, level = 0):
        with self.log_sinks_lock:
            if src not in self.log_sinks:
                self.log_sinks[src] = sink
                if src in self.log_levels:
                    self.set_level(src, level)
            else:
                raise RuntimeError("The supplied log source {} is already registered".format(src))

    def pop(self, src):
        sink = None

        with self.log_sinks_lock:
            if src in self.log_sinks:
                sink = self.log_sinks.pop(src)

        if sink is not None:
            sink.cleanup()
            return True

        return False

    def log(self, sev, src, level, msg):
        with self.log_sinks_lock:
            if src in self.log_sinks:
                sink = self.log_sinks[src]
                if src in self.log_levels and level > self.log_levels[src]:
                    return
                
                sink.log(sev, src, level, msg)

    def set_level(self, src, level):
        self.log_levels[src] = int(level)

    def get_level(self, src):
        try:
            return self.log_levels[src]
        except KeyError as e:
            return None


dispatcher = LogDispatcher()

ExceptionCallStack = "__EXCEPTCALLSTACK__"

def dlog(msg, src = 'core', level = 0):
    global dispatcher
    dispatcher.log(LOG_DEBUG, src, level, msg)

def elog(msg, src = 'core', level = 0):
    global dispatcher
    dispatcher.log(LOG_ERROR, src, level, msg)

def wlog(msg, src = 'core', level = 0):
    global dispatcher
    dispatcher.log(LOG_WARN, src, level, msg)

def ilog(msg, src = 'core', level = 0):
    global dispatcher
    dispatcher.log(LOG_INFO, src, level, msg)

def rlog(msg, src = 'core', level = 0):
    global dispatcher
    if msg == ExceptionCallStack:
        msg = "\nCall stack:\n" + "".join(traceback.format_stack()) + "\n"

    dispatcher.log(LOG_RAW, src, level, msg)

def is_log_source_registered(src):
    global dispatcher
    return (src in dispatcher.log_sinks)
    
def register_log_source(src, sink, level = None):
    global dispatcher
    dispatcher[src] = sink
    
    if level is not None:
        dispatcher.set_level(src, level)
            
def deregister_log_source(src):
    global dispatcher
    dispatcher.pop(src)

def set_log_level(src, level):
    global dispatcher
    dispatcher.set_level(src, level)
    
def get_log_level(src):
    global dispatcher
    return dispatcher.get_level(src)