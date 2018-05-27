# All rights reserved by forest fairy.
# You cannot modify or share anything without sacrifice.
# If you don't agree, keep calm and don't look on text below...

__author__ = "VirtualV <github.com/virtualvfix>"
__date__ = "$Dec 9, 2015 1:16:20 PM$"

# Compile line
# sudo pip install -U cython or sudo apt-get install cython
# python bin.py build_ext --inplace

try:
    from setuptools import setup
    from setuptools import Extension
except ImportError:
    from distutils.core import setup
    from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [
    Extension("import.py", ["release_import.py"]),
]

setup(
    name='EncImport',
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
)
