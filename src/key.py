import random

from Crypto import PublicKey, Random
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA


class RSAKeys:
    def __init__(self):
        """
        :param length: key length in bits
        """
        super().__init__()
        self.key = None
        self.public_key=None

    def generate(self, password):
        """
        Generate pair of keys.
        Encrypt private key with given password and save it to file
        """
        key = RSA.generate(1024)
        private_key = key.exportKey(passphrase=password, pkcs=8)
        with open("temp/rsa_key.txt", "wb+") as file:
            file.write(private_key)
        self.public_key=key.publickey()
        self.key = key.publickey().exportKey()
        with open("keys/public_key.txt", "wb+") as file:
            file.write(self.key)

    def decrypt_private_key(self, password):
        with open("temp/rsa_key.txt", "rb") as file:
            encoded_key = file.read()
        try:
            key = RSA.importKey(encoded_key, passphrase=password)
            return key
        except ValueError:
            print("Wrong password.")
            key = RSA.generate(1024)
            return key


class InitVector:
    def __init__(self):
        self.key = self.generate()

    def generate(self):
        rndfile = Random.new()
        self.key = rndfile.read(16)


class SessionKey:
    def __init__(self):
        self.key = None
        self.encrypted_key = None

    def generate(self):
        rndfile = Random.new()
        self.key = rndfile.read(32)

    def encrypt_with_key(self, key):
        cipher_rsa = PKCS1_OAEP.new(key)
        enc_session_key = cipher_rsa.encrypt(self.key)
        return enc_session_key

    def decrypt_with_key(self, session_key, private_key):
        self.encrypted_key = session_key
        cipher_rsa = PKCS1_OAEP.new(private_key)
        try:
            self.key = cipher_rsa.decrypt(session_key)
        except ValueError:
            rndfile = Random.new()
            self.key = rndfile.read(32)

