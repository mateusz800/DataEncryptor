import tkinter as tk

class Application:
    def __init__(self):
        self._window = tk.Tk()
        self._window.geometry('500x100')
        self._create_widgets()

    def _create_widgets(self):
        self.label = tk.Label(text='Hello World')
        self.label.pack()

    def run(self):
        self._window.mainloop()
