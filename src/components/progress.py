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
        self._column = tk.Frame()
        self._bar = Progressbar(master=self._column)
        self._text = tk.StringVar()
        self._progress_label = tk.Label(self._column, textvariable=self._text)
    
    def pack_bar(self):
        self._progress_label.pack()
        self._bar.pack(fill=tk.X, padx=40)
        self._column.pack(fill=tk.X)
        
    
    def set_progress(self, value:int):
        """
        :param int value: progress value in %
        """
        if value > 100:
            value = 100
        self._bar["value"] = value
        self._text.set(f'{value}%')