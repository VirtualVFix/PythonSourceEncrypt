# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "VirtualV <github.com/virtualvfix>"
__date__ = "$Dec 9, 2015 1:16:20 PM$"

#sudo pip install -U cython             # bin lib
#sudo apt-get install cython            # bin lib
#python bin.py build_ext --inplace  # bin line

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
    name='REDImporter',
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
)
