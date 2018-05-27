# All rights reserved by forest fairy.
# You cannot modify or share anything without sacrifice.
# If you don't agree, keep calm and don't look on text below...

__author__ = "VirtualV <github.com/virtualvfix>"
__date__ = "03/30/18 16:21"

import re
import os
import sys
import struct
import platform
import importlib
from importlib import util

IMPORTER = 'EncImport'

bits = 8 * struct.calcsize("P")
current_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'x64' if bits == 64 else 'bin')

lib_list = []
lib_ext = '.so' if 'linux' in platform.system().lower() else '.pyd'

for root, _, files in os.walk(current_dir):
    for file in files:
        if file.endswith(lib_ext):
            lib_list.append(file)

# order libs
lib_list = sorted(lib_list, key=lambda text: [int(x) if x.isdigit() else 0 for x in re.search('(32|64).*?([\d]*)\.',
                                                                                              text, re.I).group(2)])
if len(lib_list) == 0:
    print('\nImporter does\'t support "{} Python x{}" !\n'.format(platform.system(), bits))

# check for debug options
debug = False
if '--debug' in sys.argv[1:] or '--sdebug' in sys.argv[1:]:
    debug = True

for i, lib in enumerate(lib_list):
    try:
        if debug:
            print('[Importer] Loading: %s' % lib)
        spec = util.spec_from_file_location('.py', os.path.join(current_dir, lib))
        if spec is None:
            raise ImportError('Importer cannot be loaded !')
        else:
            module = util.module_from_spec(spec)
            spec.loader.exec_module(module)
            sys.modules[IMPORTER] = getattr(module, IMPORTER)
            importlib.invalidate_caches()
    except:
        if i == len(lib_list)-1:
            if debug:
                print('\n[Importer] Last error:')
            raise
    else:
        if debug:
            print('[Importer] %s is loaded' % lib)
        break
