import tkinter as tk
import sys

from key import Key
from components import LocalFile, ReceivedFile, Progress
from components.password_modal_window import PasswordModalWindow
from network import ReceiveThread, send, send_key


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
        self._received_file = ReceivedFile(self._window)
        self._create_widgets()
        # call _exit fucntion when exits
        self._window.protocol("WM_DELETE_WINDOW", self._exit)
        self._window.grid_columnconfigure(1, weight=1)
        # start thread responsible to listen and receive file
        self._receive_thread = ReceiveThread(
            host='0.0.0.0', widget=self._received_file, show_modal_func=self.show_password_modal)
        self._receive_thread.start()

    def run(self):
        self._window.mainloop()

    def _create_widgets(self):
        """
        Creating widgets and putting them into screen
        """
        self._generate_key_btn = tk.Button(
            self._window, text='generate new key', command=self._generate_key)
        self._generate_key_btn.pack()
        self._send_key_btn = tk.Button(
            self._window, text='send key',state=tk.DISABLED, command=self._send_key)
        self._send_key_btn.pack()
        self._received_file.pack(pady=40)
        self._progress = Progress(self._window)
        self._local_file = LocalFile(
            master=self._window, progress_bar=self._progress)
        self._local_file.pack(pady=40)
        self._progress.pack(fill=tk.X)
        self._progress.pack_bar()

    def _generate_key(self):
        """
        generate keys and save them to the text file
        """
        self._key.generate()
        self._key.save_txt('temp/key.txt')
        self._init_vector.generate()
        self._init_vector.save_txt('temp/init_vector.txt')
        self._local_file.add_keys(self._key.key, self._init_vector.key)
        self._send_key_btn.config(state=tk.NORMAL)
    
    def set_key(self, key):
        """
        Set received key as current
        """
        self._key = key
    
    def _send_key(self):
        send_key(host='0.0.0.0', key=self._key, iv=self._init_vector.key)

    def _exit(self):
        """
        Close the window and stop all threads running in background
        """
        self._window.destroy()
        self._receive_thread.stop()
        self._receive_thread.join()

    def show_password_modal(self, key_data:bytes, iv:bytes):
        """
        Show modal window with form in which user have to type password

        :param bytes key_data: received encoded key in bytes
        """
        self._password_modal = PasswordModalWindow(set_key_func=self.set_key, iv=iv, key_data=key_data)
        self._password_modal.focus()