import ctypes
import os
import re
import socket
import SocketServer
import struct
import sys

STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12

GENERIC_READ    = 0x80000000
GENERIC_WRITE   = 0x40000000
GENERIC_EXECUTE = 0x20000000

FILE_SHARE_READ  = 0x00000001
FILE_SHARE_WRITE = 0x00000002
OPEN_EXISTING    = 0x00000003

ENABLE_LINE_INPUT = 2
ENABLE_ECHO_INPUT = 4
ENABLE_PROCESSED_INPUT = 1

_is_windows = _is_cygwin = _is_macosx = _is_linux = _is_bsdi = _is_freebsd = _is_netbsd = _is_openbsd = _is_java = _is_android = False
loaded_win32api = False
loaded_tempfile = False

def is_windows():
    global _is_windows
    if _is_windows == True:
        return _is_windows
    if (re.search(r'win(32|64)', sys.platform)) is not None:
        _is_windows = True
    else:
        _is_windows = False
    return _is_windows

def is_cygwin():
    global _is_cygwin
    if _is_cygwin == True:
        return _is_cygwin
    if (re.search(r'cygwin', sys.platform)) is not None:
        _is_cygwin = True
    else:
        _is_cygwin = False
    return _is_cygwin

def is_macosx():
    global _is_macosx
    if _is_macosx == True:
        return _is_macosx
    if (re.search(r'darwin', sys.platform)) is not None:
        _is_macosx = True
    else:
        _is_macosx = False
    return _is_macosx

def is_linux():
    global _is_linux
    if _is_linux == True:
        return _is_linux
    if (re.search(r'linux', sys.platform)) is not None:
        _is_linux = True
    else:
        _is_linux = False
    return _is_linux

def is_bsdi():
    global _is_bsdi
    if _is_bsdi == True:
        return _is_bsdi
    if (re.search(r'bsdi', sys.platform, re.IGNORECASE)) is not None:
        _is_bsdi = True
    else:
        _is_bsdi = False
    return _is_bsdi

def is_freebsd():
    global _is_freebsd
    if _is_freebsd == True:
        return _is_freebsd
    if (re.search(r'freebsd', sys.platform)) is not None:
        _is_freebsd = True
    else:
        _is_freebsd = False
    return _is_freebsd

def is_openbsd():
    global _is_openbsd
    if _is_openbsd == True:
        return _is_openbsd
    if (re.search(r'openbsd', sys.platform)) is not None:
        _is_openbsd = True
    else:
        _is_openbsd = False
    return _is_openbsd

def is_java():
    global _is_java
    if _is_java == True:
        return _is_java
    if (re.search(r'java', sys.platform)) is not None:
        _is_java = True
    else:
        _is_java = False
    return _is_java

def is_android():
    global _is_android
    if _is_android == True:
        return _is_android
    if (re.search(r'android', sys.platform)) is not None:
        _is_android = True
    else:
        _is_android = False
    return _is_android

def is_wow64():
    if is_windows() == False:
        return False
    is64 = False
    try:
        buff = "\x00" * 4
        ctypes.windll.kernel32.IsWow64Process(-1, buff)
        if (struct.unpack("<L", buff)[0] == 1):
            is64 = True
        else:
            is64 = False
    except Exception as e:
        pass
    return is64

def cygwin_to_win32(path):
    if (re.search(r'^\/cygdrive', path) is None):
        return os.popen("cygpath -w {}".format(path), "rb").read().strip()
    dir = path.split("/")
    dir.pop(0)
    dir.pop(0)
    dir0 = dir[0]
    dir0 = dir0.upper() + ":"
    dir.pop(0)
    dir.insert(0, dir0)
    return "\\".join(dir)

def open_file(url=''):
    plat = sys.platform
    if (re.search(r'cygwin', plat) is not None):
        path = cygwin_to_win32(url)
        return os.system('cmd /c explorer "{}"'.format(path))
    else:
        return open_browser(url)

def open_browser(url='https://duckduckgo.com/'):
    global loaded_win32api
    plat = sys.platform
    if (re.search(r'cygwin', plat) is not None):
        if (url[0:1] == "/"):
            return open_file(url)
        if loaded_win32api == False:
            return
        return win32api.ShellExecute(0, "open", url, None, "", 0)
    elif (re.search(r'win32', plat) is not None):
        if loaded_win32api == False:
            return
        return win32api.ShellExecute(0, "open", url, None, "", 0)
    elif (re.search(r'darwin', plat) is not None):
        return os.system("open {}".format(url))
    elif (re.search(r'android', plat) is not None):
        return os.system("am start --user 0 -a android.intent.action.VIEW -d {}".format(url))
    else:
        if 'PATH' in os.environ:
            browsers = ['xdg-open', 'sensible-browser', 'firefox', 'firefox-bin', 'opera', 'konqueror', 'chromium-browser']
            for browser in browsers:
                for path in os.environ['PATH'].split(':'):
                    if os.path.exists("{}/{}".format(path, browser)) == True:
                        return os.system("{} {} &".format(path, browser))
    return

def open_webrtc_browser(url='https://duckduckgo.com/'):
    plat = sys.platform

    if re.search(r'win32|cygwin', plat) is not None:
        paths = [
            "Google\\Chrome\\Application\\chrome.exe",
            "Mozilla Firefox\\firefox.exe",
            "Opera\\launcher.exe"
        ]

        try:
            prog_files = os.environ['ProgramFiles']
        except KeyError as e:
            prog_files = ''

        paths = map(lambda p: "{}\\{}".format(prog_files, p), paths)
        
        try:
            app_data = os.environ['APPDATA']
        except KeyError as e:
            app_data = ''

        paths.append("{}\\Google\\Chrome\\Application\\chrome.exe".format(app_data))
        
        for path in paths:
            if os.path.exists(path) == True:
                if re.search(r'chrome\.exe', path) is not None:
                    args = "--allow-file-access-from-files"
                else:
                    args = ""
                os.system(r'""{}" {} "{}""'.format(path, args, url))
                return True
    elif re.search(r'darwin', plat) is not None:
        for browser in ['Google Chrome.app', 'Firefox.app']:
            browser_path = "/Applications/{}".format(browser)
            if os.path.isdir(browser_path) == True:
                if re.search(r'Chrome', browser_path) is not None:
                    args = "--args --allow-file-access-from-files"
                else:
                    args = ""

                os.system(r'open {} -a "{}" {} &'.format(url, browser_path, args))
                return True
    elif re.search(r'android', plat) is not None:
        os.system("am start --user 0 -a android.intent.action.VIEW -d {}".format(url))
    else:
        if 'PATH' in os.environ:
            for browser in ['google-chrome', 'chrome', 'chromium', 'firefox' , 'firefox', 'opera']:
                for path in os.environ['PATH'].split(':'):
                    browser_path = "{}/{}".format(path, browser)
                    if os.path.exists(browser_path) == True:
                        if re.search(r'Chrome', browser_path) is not None:
                            args = "--allow-file-access-from-files"
                        else:
                            args = ""
                        os.system("{} {} {} &".format(browser_path, args, url))
                        return True
    return False

def getenv(var):
    global loaded_win32api
    if (is_windows() == True and loaded_win32api == True):
        func = win32api.GetEnvironmentVariable
        retval = func(var)
        return retval
    else:
        try:
            return os.environ[var]
        except Exception as e:
            return None

def setenv(var, val):
    global loaded_win32api
    if (is_windows() == True and loaded_win32api == True):
        func = win32api.SetEnvironmentVariable
        func(var, val + "\x00")
    else:
        os.environ[var] = val

def win32_python_path():
    if not (is_windows() == True and loaded_win32api == True):
        return None
    gmh = win32api.GetModuleHandle
    gmf = win32api.GetModuleFileName
    module = gmh(None)
    return gmf(module)

def win32_winexec(cmd):
    if not (is_windows() == True and loaded_win32api == True):
        return None
    exe = win32api.WinExec
    return exe(cmd, 0)

def pipe():
    if (is_windows() == False):
        rd, wr = os.pipe()
        pipe1 = os.fdopen(rd, 'rb')
        pipe2 = os.fdopen(wr, 'wb')
        return [pipe1, pipe2]

    serv = None
    port = 1023
    while (serv is None and port < 65535):
        port += 1
        try:
            serv = SocketServer.TCPServer(('127.0.0.1', port), None)
        except Exception:
            pass

    pipe1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    pipe1.connect(('127.0.0.1', port))
    pipe2 = serv.socket.accept()[0]
    serv.server_close()

    return [pipe1, pipe2]

def temp_copy(path):
    global loaded_tempfile
    if loaded_tempfile == False:
        raise RuntimeError("Missing 'tempfile' module")
    fd = open(path, "rb")
    tp = tempfile.TemporaryFile(suffix="amn")
    tp.write(fd.read())
    tp.close()
    fd.close()
    return tp

if (is_windows() == True or is_cygwin() == True):
    try:
        import win32api
        loaded_win32api = True
    except Exception as e:
        pass

try:
    import tempfile
    loaded_tempfile = True
except Exception as e:
    pass
