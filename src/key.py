import random

from Crypto import Random
from Crypto.Cipher import AES

class Key:
    def __init__(self, length: int):
        """
        :param length: key length in bits
        """
        super().__init__()
        self._length = length
        self.key = None

    def generate(self):
        """
        generate random key 
        """
        rndfile = Random.new()
        self.key = rndfile.read(self._length)

    def save_txt(self, path: str = 'output/key.txt'):
        """
        save generated key to text file

        :param str path: path where the file will be saved, defaults to 'output/ket.txt'
        """
        with open(path, 'w') as file:
            file.write(str(self.key))

    def encrypt_with_password(self, iv, password):
        """
        Encrypt key using password. It uses CBC mode. 
        Password have to be 16 bytes long. If it is not expand it.
        """
        password = self._extend_password(password)
        aes = AES.new(password, AES.MODE_CBC, iv)
        encrypted = aes.encrypt(self.key)
        return encrypted
    
    def decrypt_with_password(self, key,  iv, password):
        password = self._extend_password(password)
        aes = AES.new(password, AES.MODE_CBC, iv)
        self.key = aes.decrypt(key)
        print(self.key)

    def _extend_password(self, password):
        """
        Extend password to te length of 16 bytes
        """
         # key must be 16, 24 or 32 bytes long
        # in our case it will be 16 bytes long so missing bytes will be equal 0
        missing_bytes = 16 - len(password)
        password_gap = ''.join(' ' for _ in range(missing_bytes))
        password += password_gap
        return password

