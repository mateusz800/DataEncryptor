import os.path
import subprocess
import tkinter as tk
from tkinter.filedialog import askopenfilename

from .file_widget import FileWidget
from file import File
from network import send


class LocalFile(FileWidget):
    """
    Allows user to select file and make some operations with it 
    such as: encrypting, sending
    """

    _iv_key = None
    _key = None

    def __init__(self, progress_bar, *args, **kwargs):
        super(LocalFile, self).__init__(*args, **kwargs)
        self._progress_bar = progress_bar

    def _pack_buttons(self):
        """
        Put buttons on the window
        """
        self._file_btn = tk.Button(
            self, text='select file', command=self._select_file)
        self._file_btn.pack(side=tk.LEFT)
        self._open_btn = tk.Button(self, text='open file', state=tk.DISABLED, command=self._open_file)
        self._open_btn.pack(side=tk.LEFT, padx=self._vertical_btn_margin)
        self._encrypt_btn = tk.Button(
            self, text='encrypt', command=self._encrypt, state=tk.DISABLED)
        self._encrypt_btn.pack(side=tk.LEFT)
        self._send_btn = tk.Button(self, text='send', command=self._send, state=tk.DISABLED)
        self._send_btn.pack(side=tk.LEFT)

    def _select_file(self):
        """
        Open file dialog and add it to the list
        """
        path = askopenfilename(
            initialdir='/', title='select file')
        self._current_file = File(path)
        self._info.insert('', 0, values=self._get_file_info(path))
        self._unlock_buttons()

    def _unlock_buttons(self):
        """
        Change status of appriopriate buttons from disabled to normal when file is selected
        """
        self._open_btn.config(state=tk.NORMAL)
        self._encrypt_btn.config(state=tk.NORMAL)

    def _encrypt(self):
        try:
            self._current_file.encrypt(key=self._key, iv=self._iv, progress_func=self._set_progress)
            self._current_file.decrypt(key=self._key, iv=self._iv)
            self._send_btn.config(state=tk.NORMAL)
        except AttributeError:
            # show message that user didn't generate keys
            print('keys are not generated')

    def _send(self):
        """
        Send the encryped file
        """
        send('0.0.0.0', self._current_file.encrypted_data)
    
    def _open_file(self, encrypted=False):
        """
        Open file in default application
        """
        print(self._current_file.path)
        try:
            os.startfile(self._current_file.path, 'open')
        except AttributeError:
            subprocess.call(['open', self._current_file.path])

    def add_keys(self, key:str, iv:str):
        """
        Add keys needed to encrypt the file
        """
        self._key = key
        self._iv = iv

    def _set_progress(self, value):
        """
        Inform progress bar about progress about some task
        """
        self._progress_bar.set_progress(value)