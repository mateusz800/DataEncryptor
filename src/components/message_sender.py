import tkinter as tk
from tkinter.scrolledtext import ScrolledText

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

    def encrypt(self):
        """
        Encrypt the message
        """
        message = self._text_input.get('1.0', tk.END)
        if self._key.key and self._iv.key:
            encryptor = MessageEncryptor(self._key.key, self._iv.key, self._mode_chooser.get_active(),
                                message, progress_func=self._progress_func)
            encryptor.start()
            encryptor.join()
        else:
            print('Keys are not generated')
        

    def send(self):
        """
        Send written messages
        """
        self.encrypt()
        mode = self._mode_chooser.get_active()
        host = self._receiver_address.get()
        if host:
            message_file = File('temp/message.txt', encrypted_mode=mode)
            send_thread = SendThread(message_file, mode=mode, host=host, show_progress_func=self._progress_func)
            send_thread.start()
        else:
            print('You have to specify receiver IP address')
