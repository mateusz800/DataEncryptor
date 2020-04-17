import socket
import threading
import os

from components.received_file import ReceivedFile


class ReceiveThread(threading.Thread):
    def __init__(self, widget: ReceivedFile, show_modal_func,  host: str = '0.0.0.0', port: int = 8080):
        """
        :param  ReceivedFile widget: widget object that shows information about received file
        :param str host: ip address of the sender ,default to 0.0.0.0 what's mean all IPv4 addresses on the local machine)
        :param int port: port, defaults to 8080
        """
        super().__init__()
        self._host: str = host
        self._port: int = port
        self._socket = socket.socket()
        self._file_widget = widget
        self._show_modal_func = show_modal_func
        self._key = None

    def run(self):
        """
        Implementation of server.
        It in infinite loop waits for connection and when the connection will
        be established receive the data and write it to the file.
        """
        self._running = True
        self._socket.bind((self._host, self._port))
        self._socket.listen()
        while self._running:
            try:
                conn, addr = self._socket.accept()
            except ConnectionAbortedError:
                break
            print('Got connection from ', addr)
            if not os.path.isdir('received_files'):
                os.makedirs('received_files')
            with conn:
                if self._key == None:
                    try:
                        self._key = conn.recv(16)
                        iv = conn.recv(16)
                        self._show_modal_func(self._key, iv)
                    except TypeError as err:
                        print(err)
                else:
                    path = f'received_files/{conn.recv(1024).decode()}'
                    with open(path, 'wb') as file:
                        while True:
                            data = conn.recv(1024)
                            if not data:
                                break
                            file.write(data)
                    self._show_modal_func()
                    self._file_widget.set_file(path, encrypted=True)

    def stop(self):
        """
        Stop the thread loop
        """
        self._running = False
        self._socket.close()

    def set_key(self, key):
        self._key = key