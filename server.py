import socket

class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostbyname(socket.getfqdn())
        self.port = 4444

    def lyssna(self, gui):        
        with self.server as s:
            s.bind((self.host, self.port))
            s.listen()

            conn, addr = s.accept()
            print('ansluten till', addr)

            # Gå vidare till att starta spelet
            gui.spela()

            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        gui.start()
                        break
                    conn.sendall(data)