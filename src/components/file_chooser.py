import os.path
import tkinter as tk
from tkinter.filedialog import askopenfilename


class FileChooser:
    """
    Allows user to choose file and checks if the file exist and if is valid
    """

    def __init__(self):
        self._file_path: str = ''
        self._pack_widgets()

    def _pack_widgets(self):
        """
        Put widgets on the window
        """
        # create widgets
        self._label = tk.Label(text='File:')
        self._file_btn = tk.Button(
            text='select', command=self._select_file)
        self._file_entry = tk.Entry()
        # add placeholder to entry
        self._file_entry.insert(0, 'no file choosen')
        self._file_entry.configure(state=tk.DISABLED)
        # put widgets on the window
        self._label.grid(row=0, column=0)
        self._file_entry.grid(row=0, column=1, sticky=tk.EW)
        self._file_btn.grid(row=0, column=2, sticky='e', padx=10)

    def _select_file(self):
        """
        Open file dialog and update label with path
        """
        self._file_path = askopenfilename(
            initialdir='/', title='select file')
        self._file_entry.configure(state=tk.NORMAL)
        self._file_entry.delete(0, tk.END)
        self._file_entry.insert(0, f'...{self._file_path[-50:]}')
        self._file_entry.configure(state=tk.DISABLED)
        self._file_entry.xview(tk.END)

    def get_file_path(self) -> str:
        """
        :return: choosen file path
        :rtype: str
        """
        if not os.path.isfile(self._file_path):
            raise Exception('file does not exist')
        return self._file_path
