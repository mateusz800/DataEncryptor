import tkinter as tk
import sys

from key import Key
from components import FilesRow, Progress, ModeChooser
from components.password_modal_window import PasswordModalWindow
from network import ReceiveThread, send_key


class Application:
    """
    Class responsible for running the entire programm
    """

    def __init__(self, width: int = 1250, height: int = 500):
        """
        :param width: width of the window (default 500)
        :param height: height of the window (default 200)
        """
        self._window = tk.Tk()
        self._window.resizable(False, False)
        self._key = Key(length=16)
        self._init_vector = Key(length=16)
        self._window.geometry('{}x{}'.format(width, height))
        self._progress = Progress(self._window)
        self._settings_frame = tk.Frame(self._window)
        self._mode_chooser = ModeChooser(master=self._settings_frame)
        self._receiver_address = tk.Entry(self._settings_frame)
        self._files_widget = FilesRow(progress_bar=self._progress, receiver_address=self._receiver_address,
                                      mode_chooser=self._mode_chooser, master=self._window)
        self._create_widgets()
        # call _exit fucntion when exits
        self._window.protocol("WM_DELETE_WINDOW", self._exit)
        self._window.grid_columnconfigure(1, weight=1)
        # start thread responsible to listen and receive file
        self._receive_thread = ReceiveThread(
            host='', widget=self._files_widget.received_file, show_modal_func=self.show_password_modal)
        self._receive_thread.start()

    def run(self):
        self._window.mainloop()

    def _create_widgets(self):
        """
        Creating widgets and putting them into screen
        """
        # first row
        # first column of the row 1 - keys
        key_frame = tk.Frame(self._settings_frame)
        self._generate_key_btn = tk.Button(
            key_frame, text='generate new key', command=self._generate_key)
        self._generate_key_btn.pack(fill=tk.X)
        self._send_key_btn = tk.Button(
            key_frame, text='send key', state=tk.DISABLED, command=self._send_key)
        self._send_key_btn.pack(fill=tk.X)
        key_frame.pack(side=tk.LEFT)
        # second column of the row 1 - receiver address
        self._receiver_address = tk.Entry(self._settings_frame)
        self._receiver_address.pack(side=tk.LEFT, padx=20)
        # third column of the row 1 - cipher mode
        self._mode_chooser.pack(side=tk.LEFT, padx=20)
        self._settings_frame.pack(fill=tk.X, padx=10)
        # third column of the row 1 - text input
        # it is written to show gui (refactoring needed)
        second_row_frame = tk.Frame()
        text_input = tk.Entry(second_row_frame)
        text_input.pack(side=tk.LEFT)
        button = tk.Button(second_row_frame, text='send message')
        button.pack(side=tk.LEFT)
        received_message = tk.Label(second_row_frame, text='Received message')
        received_message.pack(side=tk.LEFT, padx=100)
        second_row_frame.pack(fill=tk.X, pady=40, padx=10)
        # second row
        self._files_widget.pack(pady=40)
        # third row
        self._progress.pack(fill=tk.X, pady=40, side=tk.BOTTOM)
        self._progress.pack_bar()

    def _generate_key(self):
        """
        generate keys and save them to the text file
        """
        self._key.generate()
        self._key.save_txt('temp/key.txt')
        self._init_vector.generate()
        self._init_vector.save_txt('temp/init_vector.txt')
        self._files_widget.local_file.add_keys(
            self._key.key, self._init_vector.key)
        self._send_key_btn.config(state=tk.NORMAL)

    def set_key(self, key, iv):
        """
        Set received key as currents
        """
        self._key = key
        self._init_vector = Key(length=16)
        self._init_vector.key = iv
        self._files_widget.received_file.set_keys(key.key, iv)

    def _send_key(self):
        send_key(host=self._receiver_address['value'],
                 key=self._key, iv=self._init_vector.key)

    def _exit(self):
        """
        Close the window and stop all threads running in background
        """
        self._window.destroy()
        self._receive_thread.stop()
        self._receive_thread.join()

    def show_password_modal(self, key_data: bytes, iv: bytes):
        """
        Show modal window with form in which user have to type password

        :param bytes key_data: received encoded key in bytes
        """
        self._password_modal = PasswordModalWindow(
            set_key_func=self.set_key, iv=iv, key_data=key_data)
        self._password_modal.focus()
