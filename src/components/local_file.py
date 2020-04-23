import os.path
import subprocess
import tkinter as tk
from tkinter.filedialog import askopenfilename

from .file_widget import FileWidget
from file import File
from network import SendThread


class LocalFile(FileWidget):
    """
    Allows user to select file and make some operations with it 
    such as: encrypting, sending
    """

    _iv_key = None
    _key = None

    def __init__(self, progress_bar, receiver_address,  mode_chooser, *args, **kwargs):
        super(LocalFile, self).__init__(name='Choosen file', *args, **kwargs)
        self._progress_bar = progress_bar
        self._mode_chooser = mode_chooser
        self._receiver_address = receiver_address

    def _pack_buttons(self):
        """
        Put buttons on the window
        """
        self._file_btn = tk.Button(
            self, text='select file', command=self._select_file)
        self._file_btn.pack(side=tk.LEFT)
        self._open_btn = tk.Button(
            self, text='open file', state=tk.DISABLED, command=self._open_file)
        self._open_btn.pack(side=tk.LEFT, padx=self._vertical_btn_margin)
        self._encrypt_btn = tk.Button(
            self, text='encrypt', command=self._encrypt, state=tk.DISABLED)
        self._encrypt_btn.pack(side=tk.LEFT)
        self._send_btn = tk.Button(
            self, text='send', command=self._send, state=tk.DISABLED)
        self._send_btn.pack(side=tk.LEFT)

    def _select_file(self):
        """
        Open file dialog and add it to the list
        """
        path = askopenfilename(
            initialdir='/', title='select file')
        self.set_file(path)

    def _unlock_buttons(self):
        """
        Change status of appriopriate buttons from disabled to normal when file is selected
        """
        self._open_btn.config(state=tk.NORMAL)
        self._encrypt_btn.config(state=tk.NORMAL)
        self._file_btn.config(state=tk.NORMAL)
        self._send_btn.config(state=tk.NORMAL)

    def _lock_buttons(self):
        """
        Lock buttons when system is busy (file encryption or sending) to prevent taking new actions
        """
        self._file_btn.config(state=tk.DISABLED)
        self._open_btn.config(state=tk.DISABLED)
        self._encrypt_btn.config(state=tk.DISABLED)
        self._send_btn.config(state=tk.DISABLED)

    def _encrypt(self):
        try:
            self._lock_buttons()
            self._current_file.encrypt(
                key=self._key, iv=self._iv, mode=self._mode_chooser.get_active(), progress_func=self._set_progress, unlock_btns_func=self._unlock_buttons)
            # self._current_file.decrypt(key=self._key, iv=self._iv)
            # buttons should be unlocked when encription will be finished
        except AttributeError:
            # show message that user didn't generate keys
            print('keys are not generated')

    def _send(self):
        """
        Send the encryped file
        """
        send_thread = SendThread(file=self._current_file, host=self._receiver_address(), mode=self._mode_chooser.get_active(),
                                 show_progress_func=self._progress_bar.set_progress)
        send_thread.start()
        # send('192.168.1.130', self._current_file)

    def _open_file(self):
        """
        Open file in default application
        """
        path = self._current_file.path
        try:
            os.startfile(path, 'open')
        except AttributeError:
            subprocess.call(['open', path])

    def add_keys(self, key: str, iv: str):
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
