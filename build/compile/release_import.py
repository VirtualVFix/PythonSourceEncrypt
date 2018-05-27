# All rights reserved by forest fairy.
# You cannot modify or share anything without sacrifice.
# If you don't agree, keep calm and don't look on text below...

__author__ = "VirtualV <github.com/virtualvfix>"
__date__ = "$Dec 9, 2015 10:32:07 AM$"

import os
import sys
import logging

EXT = '.enc'

class Unbuffered(object):
    """
    Disable output buffering.
    """
    def __init__(self, stream, logger=None, level=logging.INFO):
        self.stream = stream
        self.logger = logger
        self.level = level

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()
        if self.logger is not None and data != '\n':
            self.logger.log(self.level, data)

    def __getattr__(self, attr):
        return getattr(self.stream, attr)


# configure unbuffered input
sys.stdout = Unbuffered(sys.stdout, level=logging.INFO)
sys.stderr = Unbuffered(sys.stderr, level=logging.ERROR)


class EncImport:
    """
    Release variant of importer without debug output.
    Importer based on PEP302.
    Decrypt source files and import module to global scope.
    Use "sys.meta_path.insert(0, EncImport(main_dir))" in launch file to replace default import.
    """
    def __init__(self, root_package_path):
        self.__modules_info = self.__collect_modules_info(root_package_path)

    @property
    def __name__(self):
        return self.__class__.__name__

    def find_module(self, fullname, path=None):
        if fullname in self.__modules_info:
            return self
        return None

    def load_module(self, fullname, path=None):
        if path is not None:
            for key in self.__modules_info:
                if self.__modules_info[key]['filename'] == path:
                    fullname = key

        if fullname not in self.__modules_info:
            raise ImportError(fullname or path)

        from importlib import util
        spec = util.spec_from_file_location(fullname, self.__modules_info[fullname]['filename'], loader=self)
        mod = sys.modules.setdefault(fullname, util.module_from_spec(spec))
        mod.__file__ = self.__modules_info[fullname]['filename']
        mod.__loader__ = self

        if self.is_package(fullname):
            mod.__path__ = []
            mod.__package__ = fullname
        else:
            mod.__package__ = fullname.rpartition('.')[0]

        try:
            exec(self.__get_source(fullname), mod.__dict__)
        except Exception as e:
            del sys.modules[fullname]
            raise ImportError(fullname) from e
        return mod

    def is_package(self, fullname):
        return self.__modules_info[fullname]['ispackage']

    def __get_source(self, fullname):
        import base64
        import hashlib

        def decode(key, enc):
            dec = []
            m_key = hashlib.sha256(key).hexdigest()
            enc = base64.urlsafe_b64decode(enc).decode()
            for i in range(len(enc)):
                key_c = m_key[i % len(m_key)]
                dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
                dec.append(dec_c)
            return "".join(dec)

        filename = self.__modules_info[fullname]['filename']
        try:
            with open(filename, 'r') as fread:
                if filename.endswith('.py'):
                    src = fread.read()
                else:
                    # Encrypt key to decode source file
                    src = decode(base64.b64decode(b'U0cxdGJVbDBTWE5NYjI5clRHbHJaVXRsZVE9PQ=='), fread.read())
        except IOError:
            src = ''

        return src

    def __collect_modules_info(self, root_package_path):
        modules = {}
        for root, _, files in os.walk(os.path.abspath(root_package_path)):
            if os.path.split(root_package_path)[0] == root:
                p_fullname = ''
            else:
                p_fullname = root.rpartition(root_package_path)[2].replace(os.sep, '.')
            filename = os.path.join(root, '__init__' + EXT)

            modules[p_fullname if not p_fullname.startswith('.') else p_fullname[1:]] = {
                'filename': filename,
                'ispackage': True
            }

            for f in files:
                if f.endswith((EXT, '.py')):
                    if f.endswith('.py') and f[:-3]+EXT in files and EXT != '.py':
                        continue

                    filename = os.path.join(root, f)
                    fullname = '.'.join([p_fullname, os.path.splitext(f)[0]]) \
                               if p_fullname != '' else os.path.splitext(f)[0]

                    modules[fullname if not fullname.startswith('.') else fullname[1:]] = {
                        'filename': filename,
                        'ispackage': False
                    }
        return modules
