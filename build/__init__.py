# All rights reserved by forest fairy.
# You cannot modify or share anything without sacrifice.
# If you don't agree, keep calm and don't look on text below...

__author__ = "VirtualV <github.com/virtualvfix>"
__date__ = "07/10/17 13:16"


import platform
from pkg_resources import parse_version

# check python version
PYTHON_MINIMAL_VERSION_SUPPORT = '3.5'
if parse_version(platform.python_version()) < parse_version(PYTHON_MINIMAL_VERSION_SUPPORT):
    raise ImportError('Incompatible python version ! Minimum require: %s; Found: %s'
                      % (PYTHON_MINIMAL_VERSION_SUPPORT, platform.python_version()))

from build.debug_import import EncImport

__all__ = ['EncImport']
