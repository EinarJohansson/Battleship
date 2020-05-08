import socket


class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostbyname(socket.getfqdn())
        self.port = 4444

    def lyssna(self, gui):
        with self.server as s:
            try:
                s.bind((self.host, self.port))
                s.listen()
            except Exception:
                gui.start()

            self.conn, self.addr = s.accept()

            with self.conn:
                print('Connected by', self.addr)
                # Gå vidare till att starta spelet
                gui.spela()
                while True:
                    data = self.conn.recv(1024)
                    if not data:
                        gui.start()
                        if hasattr(self, 'p1_starta') and hasattr(self, 'p2_starta'):
                            self.p1_starta = False
                            self.p2_starta = False
                        elif hasattr(self, 'p1_starta'):
                            self.p1_starta = False
                        elif  hasattr(self, 'p2_starta'):
                            self.p2_starta = False
                        break
                        
                    # kolla om de är redo att starta
                    data_str = str(data.decode('utf-8')).strip()

                    print('p1 är redo?', hasattr(self, 'p1_starta'))

                    if data_str == 'redo':
                        self.p2_starta = True
                    
                    print('p2 är redo?', hasattr(self, 'p2_starta'))

                    if hasattr(self, 'p2_starta') and hasattr(self, 'p1_starta'):
                        print('båda är anslutna!!!')
                        gui.redo.pack_forget()


                    
                    # hantera datat som kommer in
                    # self.conn.sendall(data)
            

    def redo(self, gui):
        try:
            self.conn.send(b'redo')
            self.p1_starta = True
        except Exception:
            gui.start()
            return
        
        if hasattr(self, 'p1_starta') and hasattr(self, 'p2_starta'):
            print('båda är anslutna!!!')
            gui.redo.pack_forget()
