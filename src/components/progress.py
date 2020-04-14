import tkinter as tk
from tkinter.ttk import Progressbar

class Progress(tk.Frame):
    """
    Widget for showing progress of a given tasks
    """
    def __init__(self, width: int = 10, *args, **kwargs):
        """
        :param int width: width of the progress bar, defaults to 400
        """
        super().__init__()
        self._bar = Progressbar(master=self)
    
    def pack_bar(self):
        self._bar.pack(fill=tk.X, padx=40)
    
    def set_progress(self, value:int):
        """
        :param int value: progress value in %
        """
        self._bar["value"] = value