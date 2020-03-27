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
        super().__init__(*args, **kwargs)

    def _pack_buttons(self):
        pass


