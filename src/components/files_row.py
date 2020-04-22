import tkinter as tk

from .local_file import LocalFile
from .received_file import ReceivedFile

class FilesRow(tk.Frame):
    def __init__(self, progress_bar, *args, **kwargs):
        super(FilesRow, self).__init__(*args, **kwargs)
        self.received_file = ReceivedFile(self)
        self.local_file = LocalFile(progress_bar=progress_bar, master=self)
        self.local_file.pack(side=tk.LEFT, padx=5)
        self.received_file.pack(side=tk.LEFT, padx=5)