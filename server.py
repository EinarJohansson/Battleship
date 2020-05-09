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
                    
                    '''
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
                    ''' 
                    if data:
                        # kolla om de är redo att starta
                        data_str = str(data.decode('utf-8')).strip()

                        if data_str == 'redo':
                            self.p2_starta = True
                        elif data_str == 'träff' or data_str == 'miss':
                            # Träffade vi eller missade vi?
                            print(data_str)
                        else:
                            # inkommande koordinater, kolla om det är miss eller träff
                            print(data_str)

                        if hasattr(self, 'p1_starta') and hasattr(self, 'p2_starta'):
                            print('båda är anslutna!!!')
                            gui.redo.pack_forget()
                            gui.spela()

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
                    elif data_str == 'träff' or data_str == 'miss':
                        # Träffade vi eller missade vi?
                        print('Received:', data_str)
                    else:
                        # inkommande koordinater, kolla om det är miss eller träff
                        print('Received:', data_str)

                    if hasattr(self, 'p1_starta') and hasattr(self, 'p2_starta'):
                        print('båda är anslutna!!!')
                        gui.redo.pack_forget()
                        gui.spela()

    def redo(self, gui):
        try:
            # KAN INTE för om jag inte är server har jag inte conn
            self.conn.send(b'redo')
        except Exception as e:
            try:
                # KAN INTE för om jag inte är server har jag inte conn
                self.server.sendall(b'redo')
                '''
                print(e)
                gui.start()
                return
                '''
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
        print(coord)
        '''
        try:
            coord = str(coord).encode('utf-8')
            self.conn.send(coord)
        except Exception:
            gui.start()
            return
        '''