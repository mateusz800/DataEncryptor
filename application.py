import tkinter as tk
from file_chooser import FileChooser


class Application:
    """
    Class responsible for running the entire programm
    """
    def __init__(self, width=500, height=100):
        self._window = tk.Tk()
        self._file_chooser = FileChooser()
        self._window.geometry('{}x{}'.format(width, height))
        self._create_widgets()

    def run(self):
        """
        Execute the infinite loop
        """
        self._window.mainloop()

    def _create_widgets(self):
        """
        Creating widgets and putting them into screen
        """
        self._send_btn = tk.Button(text='send')
        self._send_btn.pack()
       

 