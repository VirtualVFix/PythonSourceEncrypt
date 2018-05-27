#!/usr/bin/env python3
#encoding: utf-8

# All rights reserved by forest fairy.
# You cannot modify or share anything without sacrifice.
# If you don't agree, keep calm and don't look on text below...

__author__ = "VirtualV <github.com/virtualvfix>"
__date__ = "09/19/17 14:32"

import os
import sys

if __name__ == "__main__":
    main_dir = os.path.dirname(os.path.realpath(__file__))

    # check for debug options
    debug, sdebug = False, False
    # regular debug level
    if '--debug' in sys.argv[1:]:
        debug = True
    # lower debug level
    if '--sdebug' in sys.argv[1:]:
        sdebug = True

    # add debug import
    sys.path.append(os.path.split(os.path.dirname(os.path.realpath(__file__)))[0])
    from build import EncImport
    sys.meta_path.insert(0, EncImport(main_dir, debug=sdebug))

    # launch example
    from example import factorial_test
    factorial_test(40)
