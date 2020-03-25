import struct
import os
from Crypto.Cipher import AES


class File:
    """
    File class hold the information about file. 
    It also provides methods to encrypt or decrypth it content
    """

    def __init__(self, path: str):
        """
        :param str path: path to the file
        """
        super().__init__()
        self._path = path
        self._extension = self.get_extension()
        self._name = self.get_name()

    def get_extension(self) -> str:
        """
        :return: extension of the file
        :rtype: str
        """
        return self._path.split('.')[-1]

    def get_name(self) -> str:
        """
        :return : name of the file without extension
        :rtype: str
        """
        return self._path.split(".")[-1]

    def get_data(self) -> str:
        """
        :return str: file content
        :rtype: str
        """
        with open(self._path, 'r') as file:
            return file.read()

    def encrypt(self, key: str, iv: str, cipher: str = 'AES'):
        """
        Encrypt the file and save it to a file: name_encrypted.extension
        Key and initialization vector parameters are required.
        If key or initailization vector is not passed the exception will raise

        :param str key: key to data ecryption and decryption
        :param str iv: initialization vector
        :param str cipher: cipher mode, defaults to AES
        """
        if key == None:
            raise Exception('Not valid key')
        if iv == None:
            raise Exception('Not valid initialization key')
        aes = AES.new(key, AES.MODE_CBC, iv)
        file_size = os.path.getsize(self._path)
        with open(f'temp/{self._name}_encrypted.{self._extension}', 'wb') as fout:
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

    def decrypt(self, key: str = None, iv: str = None, cipher: str = 'AES'):
        """
        Decrypt the file and save it to a file
        Key and initialization vector parameters are required
        If key or initailization vector is not passed the exception will raise

        :param str key: key to data ecryption and decryption
        :param str iv: initialization vector
        :param str cipher: cipher mode - default AES
        """
        if key == None:
            raise Exception('Not valid key')
        if iv == None:
            raise Exception('Not valid initialization key')
        with open(f'temp/encrypted_file.{self._extension}', 'rb') as fin:
            file_size = struct.unpack('<Q', fin.read(struct.calcsize('<Q')))[0]
            iv = fin.read(16)
            aes = AES.new(key, AES.MODE_CBC, iv)
            with open(f'temp/decrypted_file.{self._extension}', 'w') as fout:
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
