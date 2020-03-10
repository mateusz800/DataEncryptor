import os.path
import tkinter as tk
from tkinter.filedialog import askopenfilename

class FileChooser:
    """
    Allows user to choose file and checks if the file exist and if is valid
    """
    def __init__(self):
        self._file_path = ''
        self._file_btn = tk.Button(
            text='select file', command=self._select_file)
        self._file_label = tk.Label(width=100)
        
        self._pack_widgets()
 
    def _pack_widgets(self):
        """
        Pack widgets on the window
        """
        self._file_label.pack()
        self._file_btn.pack()
            
    def _select_file(self):
        """
        Open file dialog
        """
        self._file_path = askopenfilename(
            initialdir='/', title='select file', filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        self._file_label.configure(text=self._file_path)
    
    def get_file_path(self):
        """
        If the file is valid return path to the file
        """
        if not os.path.isfile(self._file_path):
            raise Exception('file does not exist')
        return self._file_path