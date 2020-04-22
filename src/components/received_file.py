import os.path
import tkinter as tk
from tkinter.filedialog import askopenfilename

from file import File
from .file_widget import FileWidget


class ReceivedFile(FileWidget):
    """
    Shows received file information, and makes some operations on that file available
    """

    def __init__(self, *args, **kwargs):
        super(ReceivedFile, self).__init__('Received file', *args, **kwargs)
        self._lock_buttons()

    def _pack_buttons(self):
        self._decrypt_btn = tk.Button(
            self, text='decrypt file', command=self._decrypt_file)
        self._decrypt_btn.pack(side=tk.LEFT)

    def _lock_buttons(self):
        """
        Lock buttons when system is busy (file decryption or receiving) to prevent taking new actions
        """
        self._decrypt_btn.config(state=tk.DISABLED)

    def _unlock_buttons(self):
        """
        Lock buttons when system is busy (file decryption or receiving) to prevent taking new actions
        """
        self._decrypt_btn.config(state=tk.NORMAL)

    def _decrypt_file(self):
        """
        Decrypt received file. 
        """
        self._current_file.decrypt(self._key, self._iv)

    def set_keys(self, key, iv):
        self._key = key
        self._iv = iv
