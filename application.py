import tkinter as tk
from file_chooser import FileChooser
from key import Key
from file import File
from network import send, receive
import sys
import threading


class Application:
    """
    Class responsible for running the entire programm
    """

    def __init__(self, width: int = 500, height: int = 200):
        """
        :param width: width of the window (default 500)
        :param height: height of the window (default 200)
        """
        self._window = tk.Tk()
        self._key = Key(length=16)
        self._init_vector = Key(length=16)
        self._file_chooser = FileChooser()
        self._window.geometry('{}x{}'.format(width, height))
        self._create_widgets()

        self._window.grid_columnconfigure(1, weight=1)
        receiver = threading.Thread(target=receive, args=('0.0.0.0',))
        receiver.start()

    def run(self):
        self._window.mainloop()

    def _create_widgets(self):
        """
        Creating widgets and putting them into screen
        """
        self._generate_key_btn = tk.Button(
            text='generate key', command=self._generate_key)
        self._generate_key_btn.grid()
        self._send_btn = tk.Button(
            text='send encrypted file', command=self._encrypt)
        self._send_btn.grid()

    def _generate_key(self):
        """
        generate keys and save them to the text file
        """
        self._key.generate()
        self._key.save_txt('output/key.txt')
        self._init_vector.generate()
        self._init_vector.save_txt('output/init_vector.txt')

    def _encrypt(self):
        file = File(path=self._file_chooser.get_file_path())
        file.encrypt(key=self._key.key, iv=self._init_vector.key)
        file.decrypt(key=self._key.key, iv=self._init_vector.key)
        send('0.0.0.0', file.get_data.encode('utf-8'))
