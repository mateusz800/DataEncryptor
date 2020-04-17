import tkinter as tk

from key import Key


class PasswordModalWindow(tk.Toplevel):
    """
    Modal window with one text input, where user should type 
    password needed to decrypt key
    """

    def __init__(self, set_key_func, iv: str, key_data:bytes):
        super(PasswordModalWindow, self).__init__()
        self._set_key_func = set_key_func
        self._key_data = key_data
        self._iv = iv
        self._input = tk.Entry(self)
        self._submit_btn = tk.Button(self, text='submit', command=self._submit)
        self._input.pack()
        self._submit_btn.pack()

    def _submit(self):
        """
        Submit password and encrypt received key
        """
        password = self._input.get()
        key = Key(length=16)
        key.decrypt_with_password(self._key_data, password=password, iv=self._iv)
        self._set_key_func(key)
        self.destroy()
