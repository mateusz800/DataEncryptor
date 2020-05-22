import threading
import struct
import os
import math

from Crypto.Cipher import AES

from components.mode_chooser import ModeChooser


class Encryptor(threading.Thread):
    def __init__(self, key: str, iv: str, mode: str, progress_func=None):
        super(Encryptor, self).__init__()
        self._key = key
        self._iv = iv
        self._mode = mode
        self._progress_func = progress_func

    def _get_aes(self):
        """
        Get AES object based on the mode
        """
        for text, _ in ModeChooser.MODES:
            if self._mode == text:
                return {
                    'CBC': AES.new(self._key, AES.MODE_CBC, self._iv),
                    'ECB': AES.new(self._key, AES.MODE_ECB, self._iv),
                    'CFB': AES.new(self._key, AES.MODE_CFB, self._iv),
                    'OFB': AES.new(self._key, AES.MODE_OFB, self._iv),
                }[text]

    def run(self):
        raise NotImplementedError


class FileEncryptor(Encryptor):
    """
    Thread responsible for file encryption
    """

    def __init__(self, key: str, iv: str, mode: str, text=None, file=None, progress_func=None, unlock_file_btns=None):
        super(FileEncryptor, self).__init__(key, iv, mode, progress_func)
        self._file = file
        self._unlock_btns_func = unlock_file_btns

    def run(self):
        # for now only AES cipher
        aes = self._get_aes()
        file_size = os.path.getsize(self._file.path)
        with open(f'temp/{self._file.name}_encrypted.{self._file.extension}', 'wb') as fout:
            fout.write(struct.pack('<Q', file_size))
            fout.write(self._iv)
            with open(self._file.path, 'rb') as fin:
                chunk_size = 2048  # must be divided by 16
                read_size = 0  # how many is already read
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
                        self._progress_func(int((read_size/file_size) * 100))
        self._unlock_btns_func()
        return True


class MessageEncryptor(Encryptor):
    """
    Thread responsible for file encryption
    """

    def __init__(self, key: str, iv: str, mode: str, message=None, progress_func=None):
        super(MessageEncryptor, self).__init__(key, iv, mode, progress_func)
        self._message = message

    def run(self):
        # for now only AES cipher
        aes = self._get_aes()
        binary_message = self._message.encode()
        with open('temp/message_encrypted.txt', 'wb') as fout:
            fout.write(struct.pack('<Q', len(binary_message)))
            fout.write(self._iv)
            
            chunk_size =  256 # must be divided by 16
            read_size = 0  # how many is already read
            for i in range(1, math.ceil(len(binary_message)/chunk_size)): # +2
                encd = aes.encrypt(binary_message[(i-1)*chunk_size:i*chunk_size])
                fout.write(encd)
                if self._progress_func:
                    self._progress_func(int((read_size/len(binary_message)) * 100))
        return True
