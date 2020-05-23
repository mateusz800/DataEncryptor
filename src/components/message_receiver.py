import tkinter as tk
from tkinter.scrolledtext import ScrolledText

from file import File

class MessageReceiver(tk.Frame):
    """
    Component responsible for get a message from an input, encrypt it and send it
    """
    def __init__(self, *args, **kwargs):
        super(MessageReceiver, self).__init__(*args, **kwargs)
        self._label = tk.Label(self, text='Received message:')
        self._text_input = ScrolledText(self, height=3, state=tk.DISABLED)
        self._pack_widgets()

    def _pack_widgets(self):
        self._label.pack(side=tk.TOP)
        self._text_input.pack(padx=10)

    def set_message(self, message_file, encrypted_mode):
        """
        Set encrypted message
        """
        file = File(message_file, encrypted_mode=encrypted_mode)
        file.encrypt(self._key, self._iv)
        self._text_input.insert(tk.INSERT, file.encrypted)

    def set_keys(self, key, iv):
        self._key = key
        self._iv = iv