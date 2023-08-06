import compat
import copy
import os
import re

def join_unix_path(*paths):
    new_path = '/'.join(list(paths))
    while re.search("//", new_path) is not None:
        new_path = re.sub("//", "/", new_path)
    return new_path
    
def join_win_path(*paths):
    s = '\\'.join(list(paths))
    
    while s.find('\\\\') != -1:
        s.replace('\\\\', '\\')
        
    if re.search(r'\\$', s) is not None:
        trailing_slash = '\\'
    else:
        trailing_slash = ''
        
    s = s.split('\\')
    
    prefix = re.sub(r'[\*<>\?\/]', '', s[0])
    
    s.pop(0)
    
    s = map(lambda e: re.sub(r'["\*:<>\?\\\/|]', '', e), s)
    
    s.insert(0, prefix)
    
    s = '\\'.join(s)
    
    return s + trailing_slash
    

def clean_path(old):
    path = copy.copy(old)
    
    leading = r'\A\.\.\\|\A\.\.\/'
    linux_style = r'\/\.\.\/|\/\.\.\\'
    windows_style = r'\/\.\.\/|\/\.\.\\'
    
    while re.search(leading, path) is not None or re.search(linux_style, path) is not None or re.search(windows_style, path) is not None:
        path = re.sub(leading, '', path)
        path = re.sub(linux_style, '/', path)
        path = re.sub(windows_style, '\\', path)
        
    return path
    
def find_full_path(file_name):
    if (file_name[0:1] == "/" and os.path.exists(file_name) == True):
        return file_name
            
    path = compat.getenv('PATH')
    if path is not None:
        for base in path.split(os.pathsep):
            try:
                mach = re.search(r'^"(.*)"$', base)
                if mach is not None:
                    base = mach.group(1)
                path = os.path.join(base, file_name)
                if os.path.exists(path) == True and os.path.isdir(path) == False:
                    return path
            except Exception:
                pass
    return None