import socket

def send(host: str, data, port: int = 65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            conn.send(data)

def receive(host: str, port: int = 65432):
    """
    Call that function in thread
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        while True:
            print('ok')
            s.bind((host, port))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
            with open('received_file.txt', 'w') as file:
                file.write(data)