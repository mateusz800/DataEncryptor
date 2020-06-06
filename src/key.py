import random

from Crypto import PublicKey, Random
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA


class RSAKeys:
    def __init__(self):
        """
        :param length: key length in bits
        """
        super().__init__()
        self.key = None

    def generate(self, password):
        """
        Generate pair of keys.
        Encrypt private key with given password and save it to file
        """
        key = RSA.generate(2048)
        private_key = key.exportKey(passphrase=password, pkcs=8)
        with open ("keys/rsa_key.bin", "wb+") as file:
            file.write(private_key)
        self.key = key.publickey().exportKey()
        with open ("keys/public_key.txt", "wb+") as file:
            file.write(self.key)

    def decrypt_private_key(self, password):
        encoded_key=open("keys/rsa_key.bin", "rb").read()
        key=RSA.importKey(encoded_key, passphrase = password)
        return key.export.key()


class InitVector:
    def __init__(self):
        self.key=self.generate()

    def generate(self):
        rndfile=Random.new()
        self.key=rndfile.read(16)

class SessionKey:
    def __init__(self):
        self.key = None      

    def generate(self):
        rndfile=Random.new()
        self.key=rndfile.read(1024)
