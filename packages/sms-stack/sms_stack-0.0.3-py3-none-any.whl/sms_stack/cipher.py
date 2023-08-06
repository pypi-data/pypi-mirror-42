import base64
import hashlib
import binascii
import os
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Util import Counter



class AESCipher:

    def int_of_string(self, s):
        return int(binascii.hexlify(s), 16)
    
    def encrypt_message(self, key, plaintext):
        iv = Random.new().read(AES.block_size)
        key_enc = self.generate_key(key)
        ctr = Counter.new(128, initial_value=int.from_bytes(iv, byteorder='big'))
        aes = AES.new(key_enc, AES.MODE_CTR, counter=ctr)
        return base64.b64encode(iv + aes.encrypt(plaintext.encode()))
    
    def decrypt_message(self, key, ciphertext):
        enc = base64.b64decode(ciphertext)
        iv, encrypted = enc[:AES.block_size], enc[AES.block_size:]
        key_enc = self.generate_key(key)
        ctr = Counter.new(128, initial_value=int.from_bytes(iv, byteorder='big'))
        aes = AES.new(key_enc, AES.MODE_CTR, counter=ctr)
        return aes.encrypt(encrypted).decode('utf-8')

    def generate_key(self, key):
        return hashlib.sha256(key.encode()).digest()
