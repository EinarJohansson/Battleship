import socket

class Client:
    def __init__(self, host):
        self.handtag = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_host = host # Server ip
        self.server_port = 4444 # Server port
         
    def anslut(self):
        with self.handtag as s:
            s.connect((self.server_host, self.server_port))
            s.sendall(b'Hello, world')
            data = s.recv(1024)

        print('Received', repr(data))