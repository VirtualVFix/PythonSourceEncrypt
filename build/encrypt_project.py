# All rights reserved by forest fairy.
# You cannot modify or share anything without sacrifice.
# If you don't agree, keep calm and don't look on text below...

__author__ = "VirtualV <github.com/virtualvfix>"
__date__ = "09/22/17 14:23"

# copy to launch script:
# import sys
# from importer import EncImport
# sys.meta_path.insert(0, EncImport(main_dir))

import os
import sys
import base64
import shutil
import hashlib
from replace_comments import replaceComments
from optparse import OptionParser, OptionGroup


# ------------------ disable output buffering -----------------------
class Unbuffered:
    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)
# -------------------------------------------------------------------


sys.stdout = Unbuffered(sys.stdout)
# ----------------------- Encrypt variables -------------------------
# Project folder to encrypt
input_folder = 'src'
# Folder to save encrypt project
encrypt_folder = 'src_enc'
# Files extensions to encrypt
encrypt_extensions = ('.py',)
# Encrypted files extension
encrypt_output_extension = '.enc'
# Encryption key encoded to base64.
encrypt_key = b'U0cxdGJVbDBTWE5NYjI5clRHbHJaVXRsZVE9PQ=='
# Files and folders to ignore encryption, just copy.
encrypt_ignore = [
                  input_folder + os.sep + 'launcher.py',                # Base launcher
                  input_folder + os.sep + 'debug.py',                   # Debug launcher
                  os.sep + 'apk' + os.sep,                              # All apk folders
                  "__pycache__",                                        # Python cache
                  input_folder + os.sep + 'importer'                    # Compiled importer to decode source
]
# Everything which was not encrypted will be copied except this list
copy_ignore = [
               '.credentials',                                          # All credentials
               "__pycache__",                                           # Python cache
               'debug.py',                                              # Debug launcher
               'debug_import.py',                                       # Decode source modules files
               'importer_compile.py',
               'encrypt_project.py',
               'encrypt_fileordir.py',
               'bin.py',
]
# Directory of source files
main_dir = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]
# -------------------------------------------------------------------

# ------------------------ Encrypt options --------------------------
parser = OptionParser(usage='%prog [options] arg1', version='Encrypt project')
group = OptionGroup(parser, 'Test information options:')
group.add_option('-d', '--dir', dest='dir', default=None, help='Directory to save encrypted project')
group.add_option('-t', '--test', dest='test', action="store_true", default=False,
                 help='Decrypt files after encrypt for test.')
group.add_option('-r','--remove', dest='remove', action="store_true", default=False,
                 help='Remove folder for encrypt if exists !')
parser.add_option_group(group)
# -------------------------------------------------------------------

options, args = parser.parse_args()
# encryption dir
if options.dir is not None:
    if options.dir == input_folder:
        parser.print_help()
        print('Encryption directory should be different of project source: [--dir] option.')
        sys.exit()
    encrypt_folder = options.dir

# encrypt directory path
encrypt_dir = os.path.join(main_dir, encrypt_folder)

# remove enc dir
if options.remove and os.path.exists(encrypt_dir):
    answer = input('[%s] directory will be removed ! Continue ? (y/n)' % encrypt_dir)
    # clear Email class if no need send report
    if len(answer) != 0 and (answer[0].lower() in ['y', 'yes']):
        os.remove(encrypt_dir)

# make encrypt directory
if not os.path.exists(encrypt_dir):
    os.mkdir(encrypt_dir)

print('Encrypt directory: ' + os.path.join(main_dir, input_folder))
print('Encrypt output directory: ' + encrypt_dir + os.sep)
print('')


def encode(key, data):
    """ Simple encryption """
    enc = []
    m_key = hashlib.sha256(key).hexdigest()
    for i in range(len(data)):
        key_c = m_key[i % len(m_key)]
        enc_c = chr((data[i] + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode('utf-8'))


# mkdir and copy not encrypted files
for root, dirs, files in os.walk(os.path.join(main_dir, input_folder)):
    if len([x for x in copy_ignore if x in root]) == 0:
        _enc_dir = root.replace(os.path.join(main_dir, input_folder), encrypt_dir)
        if not os.path.exists(_enc_dir):
            os.mkdir(_enc_dir)
        for file in files: # copy not encrypted files
            _enc_file_path = os.path.join(root, file)
            if (not file.endswith(encrypt_extensions) or len([x for x in encrypt_ignore if x in root]) > 0
                or len([x for x in encrypt_ignore if x in _enc_file_path]) > 0) and not file.endswith('.pyc') \
                    and len([x for x in copy_ignore if x in _enc_file_path]) == 0:
                shutil.copyfile(_enc_file_path, os.path.join(_enc_dir, file))


# encrypt files
for root, _, files in os.walk(os.path.join(main_dir, input_folder)):
    if len([x for x in encrypt_ignore if x in root]) == 0:
        _enc_dir = root.replace(os.path.join(main_dir, input_folder), encrypt_dir)
        for file in files:
            if len([x for x in encrypt_ignore if x in os.path.join(root, file)]) == 0:
                if file.endswith(encrypt_extensions):
                    print('Encoding %s -> %s' % (os.path.join(root, file).replace(main_dir,''),
                                                 os.path.join(_enc_dir, file[:file.rfind('.')]
                                                              + encrypt_output_extension).replace(main_dir, '')))
                    with open(os.path.join(root, file), 'rb') as fread:
                        with open(os.path.join(_enc_dir, file[:file.rfind('.')]+encrypt_output_extension), 'wb') as fwrite:
                            lines = fread.read()
                            # write encrypt line
                            fwrite.write(encode(base64.b64decode(encrypt_key), replaceComments(lines)))


# decode test:
if options.test:
    print('')
    print("DECODING MODE IS ACTIVE !")
    print('')

    def decode(key, enc):
        dec = []
        m_key = hashlib.sha256(key).hexdigest()
        enc = base64.urlsafe_b64decode(enc).decode()
        for i in range(len(enc)):
            key_c = m_key[i % len(m_key)]
            dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
            dec.append(dec_c)
        return ''.join(dec).encode('utf-8')

    for root, _, files in os.walk(encrypt_dir):
       for file in files:
           if file.endswith(encrypt_output_extension):
               print('Decript "{}" to "{}"'.format(file, file[:file.rfind('.')]+'.py'))
               with open(os.path.join(root, file), 'rb') as fread:
                   with open(os.path.join(root, file[:file.rfind('.')]+'.py'), 'wb') as fwrite:
                       fwrite.write(decode(base64.b64decode(encrypt_key), fread.read()))
    print('')
    print("DECODING MODE IS ACTIVE !")
