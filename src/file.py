import struct
import os

from Crypto.Cipher import AES

from encryptor import Encryptor


class File:
    """
    File class hold the information about file. 
    It also provides methods to encrypt or decrypth it content
    """
    _size_prefix = ('B', 'KB', 'MB', 'GB')

    def __init__(self, path: str, encrypted=False):
        """
        :param str path: path to the file
        """
        super().__init__()
        self.path = path
        self.encrypted = encrypted

    def __getattr__(self, attr):
        """
        Available attributes:
            extension - file extension
            name - file name without extension
            data - file content (str)
            size - file size in appropriate unit
            encrypted_data - encrypted file content
        """
        if attr == 'extension':
            return self.path.split('.')[-1]
        elif attr == 'name':
            return self.path.split("/")[-1].split('.')[0]
        elif attr == 'data':
            with open(self.path, 'r') as file:
                return file.read()
        elif attr == 'encrypted_data':
            with open(f'temp/{self.name}_encrypted.{self.extension}', 'rb') as file:
                return file.read()
        elif attr == 'size':
            return self.__calculate_size()
        else:
            raise AttributeError

    def __dir__(self):
        return ('path', 'name', 'extension', 'data')

    def __calculate_size(self):
        size = os.path.getsize(self.path)
        size_prefix_index = 0
        while(size / 1000 >= 1):
            size /= 1000
            size_prefix_index += 1
        return f"{round(size, 2)} {self._size_prefix[size_prefix_index]}"

    def encrypt(self, key: str, iv: str, cipher: str = 'AES', progress_func=None, unlock_btns_func=None):
        """
        Encrypt the file and save it to a file: name_encrypted.extension
        Key and initialization vector parameters are required.
        If key or initailization vector is not passed the exception will raise

        :param str key: key to data ecryption and decryption
        :param str iv: initialization vector
        :param str cipher: cipher mode, defaults to AES
        """
        # for now only AES cipher
        encryption_thread = Encryptor(
            self, key, iv, cipher, progress_func, unlock_btns_func)
        self.encrypted = encryption_thread.start()
        return self.encrypted

    def decrypt(self, key: str, iv: str, cipher: str = 'CBC'):
        """
        Decrypt the file and save it to a file
        Key and initialization vector parameters are required
        If key or initailization vector is not passed the exception will raise

        :param str key: key to data ecryption and decryption
        :param str iv: initialization vector
        :param str cipher: cipher mode - default CBC
        """
        with open(f'temp/{self.name}_encrypted.{self.extension}', 'rb') as fin:
            file_size = struct.unpack('<Q', fin.read(struct.calcsize('<Q')))[0]
            iv = fin.read(16)
            aes = AES.new(key, AES.MODE_CBC, iv)
            with open(f'temp/{self.name}_decrypted.{self.extension}', 'w') as fout:
                while True:
                    data = fin.read(-1)
                    n = len(data)
                    if n == 0:
                        break
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