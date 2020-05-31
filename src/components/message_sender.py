import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import time

from encryptor import MessageEncryptor
from file import File
from network import SendThread


class MessageSender(tk.Frame):
    """
    Component responsible for get a message from an input, encrypt it and send it
    """

    def __init__(self, key: str, iv: str, progress_func, mode_chooser, receiver_address, *args, **kwargs):
        super(MessageSender, self).__init__(*args, **kwargs)
        self._key = key
        self._iv = iv
        self._progress_func = progress_func
        self._mode_chooser = mode_chooser
        self._receiver_address = receiver_address
        self._label = tk.Label(self, text='Write some message below')
        self._text_input = ScrolledText(self, height=3)
        self._button = tk.Button(self, text='send message', command=self.send)
        self._pack_widgets()

    def _pack_widgets(self):
        self._label.pack(side=tk.TOP)
        self._text_input.pack(side=tk.TOP, padx=10)
        self._button.pack(side=tk.RIGHT, padx=10)

    def send(self):
        """
        Send written messages
        """
        mode = self._mode_chooser.get_active()
        host = self._receiver_address.get()
        if not (self._key.key and self._iv.key):
            print('Keys are not generated')
            return
        if host:
            path = 'temp/message.txt'
            self._save_message_to_file(path)
            message_file = File(path)
            message_file.encrypt(self._key.key, self._iv.key,
                                 mode=mode, progress_func=self._progress_func)
            time.sleep(.1)
            send_thread = SendThread(
                message_file, mode=mode, host=host, show_progress_func=self._progress_func)
            send_thread.start()
        else:
            print('You have to specify receiver IP address')

    def _save_message_to_file(self, path):
        """
        Save message data to file given by a path
        """
        message = self._text_input.get('1.0', tk.END)
        with open(path, 'w') as file:
            file.write(message)

    def set_keys(self, key, iv):
        self._key = key
        self._iv = iv