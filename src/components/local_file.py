import os.path
import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename

from file import File
from network import send


class LocalFile(tk.Frame):
    """
    Allows user to select file and make some operations with it 
    such as: encrypting, sending
    """
    _columns = ('name', 'type', 'encrypted', 'size')
    _size_prefix = ('B', 'KB', 'MB', 'GB')
    _vertical_btn_margin = 5
    _iv_key = None
    _key = None

    def __init__(self, *args, **kwargs):
        super(LocalFile, self).__init__(*args, **kwargs)
        self._pack_widgets()
        self._current_file = None

    def _pack_widgets(self):
        """
        Put widgets on the window
        """
        self._info = ttk.Treeview(
            self, columns=self._columns, show='headings', height=1)
        for col in self._columns:
            self._info.heading(col, text=col)
            self._info.column(col, anchor=tk.CENTER)

        self._info.pack()
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
        self._info.insert('', tk.END, values=self._get_file_info(path))
        self._unlock_buttons()

    def _unlock_buttons(self):
        """
        Change status of appriopriate buttons from disabled to normal when file is selected
        """
        self._open_btn.config(state=tk.NORMAL)
        self._encrypt_btn.config(state=tk.NORMAL)

    def _get_file_info(self, path: str):
        """
        returns file metadata in tuple:
            (file_name, file_type, is_encrypted, file_size)
        """
        file_name = path.split('/')[-1]
        extension = file_name.split('.')[-1]
        size = os.path.getsize(path)
        _size_prefix_index = 0
        while(size / 1000 >= 1):
            size /= 1000
            _size_prefix_index += 1

        return (file_name, extension, 'False', f'{round(size, 2)} {self._size_prefix[_size_prefix_index]}')

    def _encrypt(self):
        try:
            self._current_file.encrypt(key=self._key, iv=self._iv)
            self._send_btn.config(state=tk.NORMAL)
        except AttributeError:
            # show message that user didn't generate keys
            print('keys are not generated')

    def _send(self):
        """
        Send the encryped file
        """
        send('0.0.0.0', self._current_file.get_data().encode('utf-8'))
    
    def _open_file(self, encrypted=False):
        """
        Open file in default application
        """
        try:
            os.startfile(self._current_file, 'open')
        except AttributeError:
            subprocess.call(['open', self._current_file])

    def add_keys(self, key:str, iv:str):
        """
        Add keys needed to encrypt the file
        """
        self._key = key
        self._iv = iv