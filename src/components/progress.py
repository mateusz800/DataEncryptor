import tkinter as tk
from tkinter.ttk import Progressbar

class Progress:
    """
    Widget for showing progress of a given tasks
    """
    def __init__(self, width: int = 400):
        """
        :param int width: width of the progress bar, defaults to 400
        """
        super().__init__()
        self._bar = Progressbar(length=width)
        self._bar.pack()