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
                gui.placera_skepp()
                while True:
                    try:
                        data = self.conn.recv(1024)
                    except Exception:
                        gui.start()
                        return
    
                    if data:
                        # kolla om de är redo att starta
                        data_str = str(data.decode('utf-8')).strip()

                        if data_str == 'redo':
                            self.p2_starta = True
                            if hasattr(self, 'p1_starta') and hasattr(self, 'p2_starta'):
                                print('båda är anslutna!!!')
                                gui.redo.pack_forget()
                                gui.spela()
                        elif data_str == 'träff' or data_str == 'miss':
                            # Träffade vi eller missade vi?
                            print(data_str)
                        else:
                            # inkommande koordinater, kolla om det är miss eller träff
                            print(data_str)

    def anslut(self, gui, host):
        with self.server as s:
            try:
                s.connect((host, 4444))
            except Exception as e:
                print(e)
                gui.start()
                return
            
            gui.placera_skepp()

            while True:                
                data = s.recv(1024)
                if data:
                    data_str = str(data.decode('utf-8')).strip()

                    print('Received:', data_str)

                    if data_str == 'redo':
                        self.p2_starta = True
                        if hasattr(self, 'p1_starta') and hasattr(self, 'p2_starta'):
                            print('båda är anslutna!!!')
                            gui.redo.pack_forget()
                            gui.spela()
                    elif 'träff' in data_str or 'miss' in data_str:
                        # kolla om gissningen träffade eller missade 
                        print(data_str)
                        print('vi träffade eller missade!')
                    else:
                        # inkommande koordinater, kolla om det är miss eller träff
                        print(data_str)
                        print('träffade eller missade vår motståndare?')
    
    def redo(self, gui):
        try:
            self.conn.send(b'redo')
        except Exception as e:
            try:
                self.server.sendall(b'redo')
            except Exception as e:
                print(e)
                gui.start()
                return
                 
        self.p1_starta = True

        if hasattr(self, 'p2_starta'):
            print('båda är anslutna!!!')
            gui.redo.pack_forget()
            gui.spela()

    def gissa(self, gui, coord):
        # Returnera True om vi gissa rätt, annars fel.
        try:
            coord = str(coord).encode('utf-8')
            self.conn.send(coord)
        except Exception:
            self.server.send(coord)
        
