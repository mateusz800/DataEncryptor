import struct
import os
from Crypto.Cipher import AES


class File:
    def __init__(self, path: str):
        super().__init__()
        self._path = path
        self._extension = self.get_extension()

    def get_extension(self):
        return self._path.split('.')[-1]

    def encrypt(self, cipher='AES', key: str = None, iv: str = None):
        """
        Encrypt the file and save it to a temporary file
        Key and initialization vector parameters are required
        """
        if key == None:
            raise Exception('Not valid key')
        if iv == None:
            raise Exception('Not valid initialization key')
        aes = AES.new(key, AES.MODE_CBC, iv)
        file_size = os.path.getsize(self._path)
        with open(f'encrypted_file.{self._extension}', 'wb') as fout:
            fout.write(struct.pack('<Q', file_size))
            fout.write(iv)
            with open(self._path, 'r') as fin:
                chunk_size = 2048  # must be divided by 16
                while True:
                    data = fin.read(chunk_size)
                    n = len(data)
                    if n == 0:
                        break
                    elif n % 16 != 0:
                        # file size must be divided by 16
                        data += ' ' * (16 - n % 16)
                    encd = aes.encrypt(data)
                    fout.write(encd)

    def decrypt(self, cipher='AES', key: str = None, iv: str = None):
        if key == None:
            raise Exception('Not valid key')
        if iv == None:
            raise Exception('Not valid initialization key')
        with open(f'encrypted_file.{self._extension}', 'rb') as fin:
            file_size = struct.unpack('<Q', fin.read(struct.calcsize('<Q')))[0]
            iv = fin.read(16)
            aes = AES.new(key, AES.MODE_CBC, iv)
            with open(f'decrypted_file.{self._extension}', 'w') as fout:
                while True:
                    data = fin.read(-1)
                    n = len(data)
                    if n == 0: break
                    elif n % 16 != 0:
                        # file size must be divided by 16
                        data += b' ' * (16 - n % 16)
                    decd = aes.decrypt(data)
                    n = len(decd)
                    if file_size > n:
                        fout.write(decd[:file_size].decode())
                    else:
                        fout.write(decd[:file_size].decode())
                    file_size -= n
