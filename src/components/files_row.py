import tkinter as tk

from .local_file import LocalFile
from .received_file import ReceivedFile


class FilesRow(tk.Frame):
    def __init__(self, receiver_address, progress_bar, mode_chooser, *args, **kwargs):
        super(FilesRow, self).__init__(*args, **kwargs)
        self.received_file = ReceivedFile(self)
        self.local_file = LocalFile(
            progress_bar=progress_bar, receiver_address=receiver_address, mode_chooser=mode_chooser, master=self)
        self.local_file.pack(side=tk.LEFT, padx=5)
        self.received_file.pack(side=tk.LEFT, padx=5)
