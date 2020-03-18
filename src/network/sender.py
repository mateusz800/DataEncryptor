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



