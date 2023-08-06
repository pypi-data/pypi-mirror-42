class StreamClosedError(IOError):
    def __init__(self, stream):
        self.stream = stream

    def __str__(self):
        try:
            return "Stream {} is closed.".format(self.stream.fileno())
        except Exception as e:
            return "Stream {} is closed.".format(self.stream)

class SocketError(Exception):
    def __str__(self):
        return "A socket error occurred."

class HostCommunicationError(object):
    def __init__(self, *args, **kwargs):
        try:
            self.host = args[0]
        except Exception:
            self.host = None
        try:
            self.port = args[1]
        except Exception:
            self.port = None

    def addr_str(self):
        if self.host is not None and self.port is not None:
            return "({}:{})".format(self.host, self.port)
        elif host is not None:
            return "({})".format(self.host)
        else:
            return ""

class ConnectionError(IOError, SocketError, HostCommunicationError):
    def __init__(self, *args):
        try:
            self.host = args[0]
        except Exception:
            self.host = None
        try:
            self.port = args[1]
        except Exception:
            self.port = None

        return super(ConnectionError, self).__init__(*args)

class ConnectionRefused(ConnectionError):
    def __init__(self, *args):
        try:
            self.host = args[0]
        except Exception:
            self.host = None
        try:
            self.port = args[1]
        except Exception:
            self.port = None

        return super(ConnectionRefused, self).__init__(*args)

    def __str__(self):
        return "The connection was refused by the remote host {}.".format(self.addr_str())

class HostUnreachable(ConnectionError):
    def __init__(self, *args):
        try:
            self.host = args[0]
        except Exception:
            self.host = None
        try:
            self.port = args[1]
        except Exception:
            self.port = None

        return super(HostUnreachable, self).__init__(*args)

    def __str__(self):
        return "Destination host {} unreachable.".format(self.addr_str())

class ConnectionTimeout(ConnectionError):
    def __init__(self, *args):
        try:
            self.host = args[0]
        except Exception:
            self.host = None
        try:
            self.port = args[1]
        except Exception:
            self.port = None

        return super(ConnectionTimeout, self).__init__(*args)

    def __str__(self):
        return "The connection timed out {}.".format(self.addr_str())

class InvalidDestination(ConnectionError):
    def __init__(self, *args):
        try:
            self.host = args[0]
        except Exception:
            self.host = None
        try:
            self.port = args[1]
        except Exception:
            self.port = None

        return super(InvalidDestination, self).__init__(*args)

    def __str__(self):
        return "The destination is invalid: {}.".format(self.addr_str())
        
class BindError(ValueError, ConnectionError):
    def __init__(self, *args):
        try:
            self.host = args[0]
        except Exception:
            self.host = None
        try:
            self.port = args[1]
        except Exception:
            self.port = None

        return super(BindError, self).__init__(*args)

    def __str__(self):
        return "The address is already in use or is unavailable: {}.".format(self.addr_str())

class AddressInUseError(ConnectionError):
    def __init__(self, *args):
        try:
            self.host = args[0]
        except Exception:
            self.host = None
        try:
            self.port = args[1]
        except Exception:
            self.port = None

        return super(AddressInUseError, self).__init__(*args)

    def __str__(self):
        return "The address is already in use or is unavailable: {}.".format(self.addr_str())
        
class UnsupportedProtocolError(ValueError, SocketError):
    def __init__(self, proto = None):
        self.proto = proto
        return super(UnsupportedProtocolError, self).__init__()

    def __str__(self):
        return "The protocol {} is not supported.".format(self.proto)
        
class ConnectionProxyError(ConnectionError):
    def __init__(self, *args):
        self.host = args[0]
        self.port = args[1]
        self.ptype = args[2]
        self.reason = args[3]
        return super(ConnectionProxyError, self).__init__(*args)

    def __str__(self):
        return self.ptype + ": " + self.reason
