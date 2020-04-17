import os
import tkinter as tk
from tkinter import ttk

from file import File



class FileWidget(tk.Frame):
    _columns = ('name', 'type', 'encrypted', 'size')

    _vertical_btn_margin = 5

    def __init__(self, *args, **kwargs):
        super(FileWidget, self).__init__(*args, **kwargs)
        self._current_file = None
        self.__pack_widgets()

    def __pack_widgets(self):
        """
        Put widgets on the window
        """
        self._info = ttk.Treeview(
            self, columns=self._columns, show='headings', height=1)
        for col in self._columns:
            self._info.heading(col, text=col)
            self._info.column(col, anchor=tk.CENTER)
        self._info.pack()
        self._pack_buttons()
    
    def _pack_buttons(self):
        raise NotImplementedError

    def _unlock_buttons(self):
        raise NotImplementedError
    
    def _get_file_info(self, path: str):
        """
        returns file metadata in tuple:
            (file_name, file_type, is_encrypted, file_size)
        """
        return (self._current_file.name, self._current_file.extension, self._current_file.encrypted, self._current_file.size)

    def _show_file_info(self, path: str):
        """
        Show information about the file

        :param str path: path to the file
        """
        self._info.insert('', 0, values=self._get_file_info(path))
    
    def set_file(self, path: str, encrypted:bool = False):
        """
        Set the file object that the widget shouls show

        :param str path: path to the file
        """
        self._current_file = File(path, encrypted)
        self._show_file_info(path)
        self._unlock_buttons()

