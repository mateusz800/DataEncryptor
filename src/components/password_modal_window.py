import tkinter as tk
import hashlib


class PasswordModalWindow(tk.Toplevel):
    """
    Modal window with one text input, where user should type 
    password needed to decrypt key
    """

    def __init__(self, set_password_func=None, onsubmit=None, decrypt_key_func=None):
        super(PasswordModalWindow, self).__init__()
        self._onsubmit = onsubmit
        self._decrypt_key_func = decrypt_key_func
        self.title("Password")
        self._set_password_func = set_password_func
        self._input = tk.Entry(self)
        self._submit_btn = tk.Button(self, text='submit', command=self._submit)
        self._input.pack()
        self._submit_btn.pack()

    def _submit(self):
        """
        Submit password and encrypt received key
        """
        password = self._input.get()
        hash_password = hashlib.sha256()
        hash_password.update(password.encode())
        if self._onsubmit:
            self._decrypt_key_func(hash_password.hexdigest())
            self._onsubmit.decrypt()
        else:
            self._set_password_func(hash_password.hexdigest())
      
        self.destroy()
