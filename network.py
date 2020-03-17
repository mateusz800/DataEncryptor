import socket

def send(host: str, data, port: int = 8080):
    """
    Implementation of client
    It send data to the other computer
    :param host: ip address of the receiver
    :param port: port
    """
    with socket.socket() as s:
        s.connect((host, port))
        s.send(data)

def receive(host: str = '0.0.0.0', port: int = 8080):
    """
    Implementation of server
    It in infinite loop waits for connection and when the connection will
    be established receive the data and write it to the file
    :param host: ip address of the sender (default 0.0.0.0 what's mean all 
        IPv4 addresses on the local machine)
    :param port: port
    """
    with socket.socket() as s:
        s.bind((host, port))
        s.listen(5)
        while True:
            conn, addr = s.accept()
            received = ''
            print('Got connection from ', addr)
            with conn:
                while True:
                    data = conn.recv(1024)
                    if not data: break
                    received += data.decode('utf-8')
            with open('received_file.txt', 'w') as file:
                file.write(received)