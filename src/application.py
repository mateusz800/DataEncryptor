import tkinter as tk
import sys

from key import Key

from components import LocalFile, ReceivedFile, Progress
from network import ReceiveThread, send


class Application:
    """
    Class responsible for running the entire programm
    """

    def __init__(self, width: int = 1000, height: int = 500):
        """
        :param width: width of the window (default 500)
        :param height: height of the window (default 200)
        """
        self._window = tk.Tk()
        self._key = Key(length=16)
        self._init_vector = Key(length=16)
        self._window.geometry('{}x{}'.format(width, height))
        self._create_widgets()

        self._window.protocol("WM_DELETE_WINDOW", self._exit)
        self._window.grid_columnconfigure(1, weight=1)
        self._receive_thread = ReceiveThread(host='0.0.0.0')
        self._receive_thread.start()

    def run(self):
        self._window.mainloop()

    def _create_widgets(self):
        """
        Creating widgets and putting them into screen
        """
        self._generate_key_btn = tk.Button(
            self._window, text='generate key', command=self._generate_key)
        self._generate_key_btn.pack(pady=20)
        self._received_file = ReceivedFile(self._window)
        self._received_file.pack(pady=40)
        self._local_file = LocalFile(self._window)
        self._local_file.pack(pady=40)
        # self._progress = Progress()
        # self._progress.pack()

    def _generate_key(self):
        """
        generate keys and save them to the text file
        """
        self._key.generate()
        self._key.save_txt('temp/key.txt')
        self._init_vector.generate()
        self._init_vector.save_txt('temp/init_vector.txt')
        self._local_file.add_keys(self._key.key, self._init_vector.key)

    def _exit(self):
        """
        Close the window and stop all threads running in background
        """
        self._window.destroy()
        self._receive_thread.stop()
        self._receive_thread.join()
