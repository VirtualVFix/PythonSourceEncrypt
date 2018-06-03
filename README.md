# Python3 source files encryption
Protect Python source files.

There are not a lot method to protect source files on Python. Project may compiled to binary file or .pyd/.so libraries by parts. Those methods are give a good protection, but any changes in source files is requred re-compile for all target platforms.
Other way to protect is **encrypt source files:**

This method based customization of the Python import mechanism described in [PEP 302](https://www.python.org/dev/peps/pep-0302/).
Compilation is required for new import module only and not required recompile until encrypt key not changed.
Unfortunately this method cannot fully protect source code because decrypted files load to Python global scope and they may be grabbed in runtime.

## Files
* **/build/compile/release_import.py** - Release version of importer to compile without debug option
* **/build/compile/compile.py**
* **/build/debug_import.py** - Debug version of importer. May work as with source as encrypted files
* **/build/encrypt_project.py** - Script for encrypt whole project
* **/build/encrypt_fileordir.py** - Script for encrypt/decrypt some file
* **/build/replace_comment.py** - Library used to replace comments and doc lines with save line count
* **/src/** - Project source files
* **/src/debug.py** - Script to launch not encrypted project via debug imporrter.
* **/src/launcher.py** - Script to launch encryped project via compiled importer (May work with encrypted files only. Should not be encrypted)   
* **/src/importer/__init__.py** - Importer loader (Should not be encrypted)
* **/src/importer/bin/** - Compiled importer for all target platforms
* **/src_enc/** - Encrypted files

## Configuration
3. Setup encrypt key to **encrypt_key** variable in **/build/encrypt_project.py** and **/build/encrypt_fileordir.py** files. Key should be encrypted by base64:
```python
import base64
base64.b64encode(b'EncryptKey')
```
2. Replace this key in the following files: **/build/debug_import.py** line 165 and **/build/compile/release_import.py** line 111
3. Compile **/build/compile/release_import.py** and copy compiled lib to **/src/importer/bin/**
4. Add import your launcher to end of **/src/launcher.py** and **/src/debug.py** files
5. Setup variables in **/build/encrypt_project.py** and encrypt your project

## Compilation
1. Install cython library: **sudo pip install -U cython** or **python3 -m pip install cython**
2. cd **/build/compile && python3 compile.py build_ext --inplace**
3. Move **.so** or **.pyd** file to **/src/importer/bin/**
    * File should have "64" or 32" in name and have extension: win32.pyd, amd64.pyd
    * Each platform may have more one compiled files. Those files should ends with digit: win32_v1.pyd, win32_v2.pyd. Another version will be used when  file cannot be import.
