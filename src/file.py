import struct
import os

from Crypto.Cipher import AES

from encryptor import FileEncryptor


class File:
    """
    File class hold the information about file. 
    It also provides methods to encrypt or decrypth it content
    """
    _size_prefix = ('B', 'KB', 'MB', 'GB')

    def __init__(self, path: str, encrypted=False, encrypted_mode=None):
        """
        :param str path: path to the file
        """
        super().__init__()
        self.path = path
        self.encrypted = encrypted
        self._encrypted_mode = encrypted_mode

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
            with open(f'files/{self.name}_encrypted.{self.extension}', 'rb') as file:
                return file.read()
        elif attr == 'decrypted_data':
            with open(f'files/{self.name}_decrypted.{self.extension}', 'rb') as file:
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

    def encrypt(self, key: str, iv: str, mode: str=None, progress_func=None, unlock_btns_func=None):
        """
        Encrypt the file and save it to a file: name_encrypted.extension
        Key and initialization vector parameters are required.
        If key or initailization vector is not passed the exception will raise

        :param str key: key to data ecryption and decryption
        :param str iv: initialization vector
        :param str cipher: cipher mode, defaults to AES
        """
        if mode == None:
            mode = self._encrypted_mode
        encryption_thread = FileEncryptor(
            self, key, iv, mode, progress_func, unlock_btns_func)
        encryption_thread.start()
        self.encrypted = True
        return self.encrypted

    def decrypt(self, key: str, iv: str, mode: str = 'CBC'):
        """
        Decrypt the file and save it to a file
        Key and initialization vector parameters are required
        If key or initailization vector is not passed the exception will raise

        :param str key: key to data ecryption and decryption
        :param str iv: initialization vector
        :param str mode: cipher mode - default CBC
        """
        # if already decrypted but with e.g. wrong password
        if(self.name.split('_')[-1]=='decrypted'):
            name = self.name.replace('_decrypted', '')
            self.path = f'{name}.{self.extension}'

        with open(f'files/{self.name}.{self.extension}', 'rb') as fin:
            file_size = struct.unpack('<Q', fin.read(struct.calcsize('<Q')))[0]
            iv = fin.read(16)
            aes = AES.new(key, self._get_aes_mode(mode), iv)
            self.path = f'files/{self.name}_decrypted.{self.extension}'
            with open(self.path, 'wb') as fout:
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
                    fout.write(decd[:file_size])
                    file_size -= n

    def _get_aes_mode(self, mode: str):
        """
        return mode compatible with Crypto.Cipher.AES
        """
        return {
            'CBC': AES.MODE_CBC,
            'ECB': AES.MODE_ECB,
            'CFB': AES.MODE_CFB,
            'OFB': AES.MODE_OFB
        }[mode]
