# All rights reserved by forest fairy.
# You cannot modify or share anything without sacrifice.
# If you don't agree, keep calm and don't look on text below...

__author__ = "VirtualV <github.com/virtualvfix>"
__date__ = "09/22/17 14:23"

import os
import sys
import base64
import hashlib
from replace_comments import replaceComments


# ---------------------- disable output buffering -------------------------------
class Unbuffered:
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)


sys.stdout = Unbuffered(sys.stdout)
# -------------------------------------------------------------------------------
# Files extensions to encrypt
encrypt_extensions = ('.py',)
# Encrypted files extension
encrypt_output_extension = '.enc'
# Encryption key encoded to base64.
encrypt_key = b'U0cxdGJVbDBTWE5NYjI5clRHbHJaVXRsZVE9PQ=='

from optparse import OptionParser, OptionGroup

parser = OptionParser(usage='%prog [options] arg1', version='Simple encrypt / decrypt file or directory')
group = OptionGroup(parser, 'Test information options:')
group.add_option('--dir', dest='dir', default=None, help='Directory or file for encrypt/decrypt')
group.add_option('--decrypt', dest='decrypt', action="store_true", default=False,
                 help='Decrypt file or directory. False by default.')
parser.add_option_group(group)    

options, args = parser.parse_args()
if not options.dir: 
    parser.print_help()
    print('You need to specify the directory or file to encrypt/decrypt: [--dir] option.')
    sys.exit()

DIRECTORY_OR_FILE = options.dir

if options.decrypt:
    def decode(key, enc):
        """ Simple decoding """
        dec = []
        m_key = hashlib.sha256(key).hexdigest()
        enc = base64.urlsafe_b64decode(enc).decode()
        for i in range(len(enc)):
            key_c = m_key[i % len(m_key)]
            dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
            dec.append(dec_c)
        return ''.join(dec).encode('utf-8')
    
    def decrypt(root, file):
        if file.endswith(encrypt_output_extension): 
            print('Decript "%s" to "%s"' % (file, file[:file.rfind('.')]+'.dec.py'))
            with open(os.path.join(root, file), 'rb') as fread:
                with open(os.path.join(root, file[:file.rfind('.')]+'.dec.py'), 'wb') as fwrite:
                    fwrite.write(decode(base64.b64decode(encrypt_key), fread.read()))


    print('')
    print("DECODING MODE IS ACTIVE !")
    print('')
    if os.path.isdir(DIRECTORY_OR_FILE):
        for root, dirs, files in os.walk(DIRECTORY_OR_FILE):
            for file in files:
                decrypt(root, file)
    else:
        root, file = os.path.split(os.path.realpath(DIRECTORY_OR_FILE))
        decrypt(root, file)                        
else:
    def encode(key, data):
        """ Simple encryption """
        enc = []
        m_key = hashlib.sha256(key).hexdigest()
        for i in range(len(data)):
            key_c = m_key[i % len(m_key)]
            enc_c = chr((data[i] + ord(key_c)) % 256)
            enc.append(enc_c)
        return base64.urlsafe_b64encode("".join(enc).encode('utf-8'))
    
    def encrypt(root, file):        
        if file.endswith(encrypt_extensions):
            print('Encoding "{}" to "{}"'.format(file, file[:file.rfind('.')]+encrypt_output_extension))
            with open(os.path.join(root, file), 'rb') as fread:
                with open(os.path.join(root, file[:file.rfind('.')]+encrypt_output_extension), 'wb') as fwrite:
                    lines = fread.read()
                    # write encrypt line    
                    fwrite.write(encode(base64.b64decode(encrypt_key), replaceComments(lines)))

    print('')
    print("ENCODING MODE IS ACTIVE !")
    print('')
    if os.path.isdir(DIRECTORY_OR_FILE):
        for root, dirs, files in os.walk(DIRECTORY_OR_FILE):
            for file in files:
                encrypt(root, file)
    else:
        root, file = os.path.split(os.path.realpath(DIRECTORY_OR_FILE))
        encrypt(root, file)
