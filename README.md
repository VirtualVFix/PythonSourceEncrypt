# Python source files encryption
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
* **/src/importer/bin/** Compiled importer for all target platforms
* **/src_enc/** - Encrypted files

