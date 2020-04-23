import threading
import struct
import os

from Crypto.Cipher import AES




class Encryptor(threading.Thread):
    """ 
    Thread responsible for file encryption 
    """
    def __init__(self, file, key: str, iv: str, mode, progress_func=None, unlock_file_btns=None):
        super(Encryptor, self).__init__()
        self._file = file
        self._key = key
        self._iv = iv
        self._mode = mode
        self._progress_func = progress_func
        self._unlock_btns_func = unlock_file_btns

    def run(self):
           # for now only AES cipher
        aes = AES.new(self._key, AES.MODE_CBC, self._iv)
        file_size = os.path.getsize(self._file.path)
        with open(f'temp/{self._file.name}_encrypted.{self._file.extension}', 'wb') as fout:
            fout.write(struct.pack('<Q', file_size))
            fout.write(self._iv)
            with open(self._file.path, 'rb') as fin:
                chunk_size = 2048  # must be divided by 16
                read_size = 0 # how many is already read
                while True:
                    data = fin.read(chunk_size)
                    n = len(data)
                    read_size += n
                    if n == 0:
                        break
                    elif n % 16 != 0:
                        # file size must be divided by 16
                        data += ' '.encode() * (16 - n % 16)
                    encd = aes.encrypt(data)
                    fout.write(encd)
                    if self._progress_func:
                        self._progress_func(int((read_size/file_size) * 100) )
        self._unlock_btns_func()
        return True
