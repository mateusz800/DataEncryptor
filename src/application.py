import sys
import tkinter as tk

from Crypto.PublicKey import RSA

from key import RSAKeys, InitVector, SessionKey
from components import FilesRow, Progress, ModeChooser, MessageSender, MessageReceiver
from components.password_modal_window import PasswordModalWindow
from network import ReceiveThread, send_request_for_key, send_session_key


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
        self._window.title("Projekt 1 - Mateusz Budnik, Paweł Żurek")
        self._window.resizable(False, False)
        self._keys = RSAKeys()
        self._init_vector = InitVector()
        self._session_key = SessionKey()
        self._window.geometry('{}x{}'.format(width, height))
        self._progress = Progress(self._window)
        self._settings_frame = tk.Frame(self._window)
        self._mode_chooser = ModeChooser(master=self._settings_frame)
        self._receiver_address = tk.Entry(self._settings_frame)
        self._files_widget = FilesRow(progress_bar=self._progress, receiver_address=self.get_receiver_address,
                                      mode_chooser=self._mode_chooser, show_modal_func=self.show_password_modal, master=self._window)
        self._second_row_frame = tk.Frame()
        self._message_receiver = MessageReceiver(master=self._second_row_frame)
        self._create_widgets()
        # call _exit fucntion when exits
        self._window.protocol("WM_DELETE_WINDOW", self._exit)
        self._window.grid_columnconfigure(1, weight=1)
        # start thread responsible to listen and receive file
        self._receive_thread = ReceiveThread(
            host='', widget=self._files_widget.received_file, message_receiver=self._message_receiver,
            get_public_key_func=self.get_receiver_public_key, decrypt_session_key_func=self.decrypt_session_key,
            show_modal_func=self.show_password_modal)
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
            key_frame, text='send session key', state=tk.DISABLED, command=self._send_request_for_public_key)
        self._send_key_btn.pack(fill=tk.X)
        key_frame.pack(side=tk.LEFT)
        # second column of the row 1 - receiver address
        receiver_address_col = tk.Frame(self._settings_frame)
        label = tk.Label(receiver_address_col, text='Receiver IP address:')
        label.pack(side=tk.TOP)
        self._receiver_address = tk.Entry(receiver_address_col)
        self._receiver_address.pack(side=tk.BOTTOM)
        receiver_address_col.pack(side=tk.LEFT, padx=20)
        # third column of the row 1 - cipher mode
        self._mode_chooser.pack(side=tk.LEFT, padx=20)
        self._settings_frame.pack(fill=tk.X, padx=10)
        # third column of the row 1 - text input
        # it is written to show gui (refactoring needed)
        self._message_sender = MessageSender(
            master=self._second_row_frame, key=self._session_key, iv=self._init_vector,
            progress_func=self._progress.set_progress, mode_chooser=self._mode_chooser, receiver_address=self._receiver_address)
        self._message_sender.pack(side=tk.LEFT)
        self._message_receiver.pack(side=tk.LEFT, pady=10)
        self._second_row_frame.pack(fill=tk.X, pady=10, padx=10)
        # second row
        self._files_widget.pack(fill=tk.X, pady=40)
        # third row
        self._progress.pack(fill=tk.X, pady=40, side=tk.BOTTOM)
        self._progress.pack_bar()

    def _send_request_for_public_key(self):
        send_request_for_key(host=self._receiver_address.get())

    def _generate_key(self):
        """
        generate keys and save them to the text file
        """
        self._init_vector.generate()
        self._password_modal = PasswordModalWindow(
            set_password_func=self.set_key_password)
        self._password_modal.focus()

    def set_key(self, key, iv):
        """
        Set received key as currents
        """
        self._session_key = key
        self._session_key.decrypt_with_password(iv, self._private_key.key)
        self._init_vector = InitVector()
        self._init_vector.key = iv
        self._files_widget.received_file.set_keys(
            self._session_key, self._init_vector)
        self._message_receiver.set_keys(self._session_key, self._init_vector)
        self._message_sender.set_keys(self._session_key, self._init_vector)

    def _send_key(self):
        # niepotrzebne
        host = self._receiver_address.get()
        if host != '' and self._password:
            send_key(host=self._receiver_address.get(),
                     key=self._session_key, iv=self._init_vector.key, password=self._password)
        elif self._password is None:
            print("You have to specify password")
        else:
            print('You have to specify a receiver IP address')

    def _exit(self):
        """
        Close the window and stop all threads running in background
        """
        self._window.destroy()
        self._receive_thread.stop()
        self._receive_thread.join()

    def show_password_modal(self):
        """
        Show modal window with form in which user have to type password

        :param bytes key_data: received encoded key in bytes
        """
        self._password_modal = PasswordModalWindow(
            set_password_func=self.set_key_password)
        self._password_modal.focus()

    def set_key_password(self, password):
        self._password = password
        self._keys.generate(password)
        self._send_key_btn.config(state=tk.NORMAL)

    def get_receiver_address(self):
        return self._receiver_address.get()

    def get_receiver_public_key(self, key):
        self._receiver_public_key = RSA.importKey(key).publickey()
        self._session_key.generate()
        self._message_receiver.set_keys(self._session_key.key, self._init_vector.key)
        self._files_widget.received_file.set_keys(self._session_key.key, self._init_vector.key)
        self._files_widget.local_file.add_keys(
            self._session_key.key, self._init_vector.key)
        encrypted = self._session_key.encrypt_with_key(
            self._receiver_public_key)
        send_session_key(self._receiver_address.get(), encrypted)

    def decrypt_session_key(self, session_key):
        private_key = self._keys.decrypt_private_key(self._password)
        self._session_key.decrypt_with_key(session_key, private_key)
        self._message_receiver.set_keys(self._session_key.key, self._init_vector.key)
        self._files_widget.received_file.set_keys(self._session_key.key, self._init_vector.key)
        self._files_widget.local_file.add_keys(self._session_key.key, self._init_vector.key)

