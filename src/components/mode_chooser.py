import tkinter as tk
from tkinter import StringVar
from tkinter.ttk import Radiobutton


class ModeChooser(tk.Frame):
    """
    Thanks to that frame user can choose in which mode the file should be encrypted
    """
    MODES = [('CBC', 1), ('ECB', 2), ('CFB', 3), ('OFB', 4)]

    def __init__(self, active_mode: str = 'CBC', *args, **kwargs):
        """
        :param str active_mode: default selected mode (default is CBC). Possible modes: ECB, CBC, CFB, OFB
        """
        super(ModeChooser, self).__init__(*args, **kwargs)
        self._active_mode = StringVar()
        self._active_mode.set(1)
        label = tk.Label(self, text='Select mode:')
        label.pack()
        for text, mode in self.MODES:
            rb = Radiobutton(
                self, text=text, variable=self._active_mode, value=mode)
            rb.pack(side=tk.LEFT)
