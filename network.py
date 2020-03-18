import socket
import threading


def send(host: str, data, port: int = 8080):
    """
    Implementation of client.
    It send data to the other computer.

    :param str host: ip address of the receiver
    :param int port: port, defaults to 8080
    """
    with socket.socket() as s:
        self._socket.connect((host, port))
        self._socket.send(data)


class ReceiveThread(threading.Thread):
    def __init__(self, host: str = '0.0.0.0', port: int = 8080):
        """
        :param str host: ip address of the sender ,default to 0.0.0.0 what's mean all IPv4 addresses on the local machine)
        :param int port: port, defaults to 8080
        """
        super().__init__()
        self._host: str = host
        self._port: int = port
        self._socket = socket.socket()

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
            received: str = ''
            print('Got connection from ', addr)
            with conn:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    received += data.decode('utf-8')
            with open('received_file.txt', 'w') as file:
                file.write(received)

    def stop(self):
        """
        Stop the thread loop
        """
        self._running = False
        self._socket.close()
