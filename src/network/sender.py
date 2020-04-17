import socket
import threading

from file import File
from key import Key


def send_key(host: str, key: Key, iv: bytes, port: int = 8080):
    """
    Send encrypted keys to other machines
    """
    encrypted_key = key.encrypt_with_password(iv, 'password')
    with socket.socket() as s:
        s.connect((host, port))
        s.send(encrypted_key)
        s.send(iv)


def send(host: str, file: File, port: int = 8080):
    """
    Implementation of client.
    It send data to the other computer.

    :param str host: ip address of the receiver
    :param int port: port, defaults to 8080
    """
    with socket.socket() as s:
        s.connect((host, port))
        file_name = f'{file.name}.{file.extension}'
        s.send(file_name.encode())
        s.send(file.encrypted_data)
