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
            except:
                gui.start()
                return

            self.conn, self.addr = s.accept()

            with self.conn:
                print('Connected by', self.addr)
                # Gå vidare till att starta spelet
                gui.placera_skepp()

                while True:
                    try:
                        data = self.conn.recv(1024)
                    except:
                        gui.start()
                        return

                    if data:
                        self.hantera(data, gui)

    def anslut(self, gui, host):
        with self.server as s:
            try:
                s.connect((host, 4444))
            except:
                gui.start()
                return

            gui.placera_skepp()

            while True:
                data = s.recv(1024)
                if data:
                    self.hantera(data, gui)

    def hantera(self, data, gui):
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

            # få fram koordinaten från strängen
            coord, sep, resultat = data_str.partition(': ')
            print('koordinaten: ', coord)
            print('resultat: ', resultat)

            coord = eval(coord)

            färg = gui.p2.itemcget(coord, 'fill')

            if resultat == 'träff':
                gui.p2.itemconfig(coord, fill='blue')
            else:
                gui.p2.itemconfig(coord, fill='red')
        else:
            # inkommande koordinater, kolla om det är miss eller träff
            print(data_str)
            print('träffade eller missade vår motståndare?')
            if self.träff(data_str, gui):
                # Skicka att det är en träff
                svar = str(data_str + ': träff')
                self.skicka(svar, gui)
            else:
                # Skicka att det är en miss
                svar = str(data_str + ': miss')
                self.skicka(svar, gui)

    def träff(self, coord, gui):
        '''Returnera sant ifall kordinaten är träffad'''

        # Gör om sträng till tupel
        coord = eval(coord)

        # Koordinatens färg
        färg = gui.p1.itemcget(coord, 'fill')

        if färg == '#9cffba':
            # rita på våran spelplan att vår motsåndare gisassde rätt på koordinaten
            gui.p1.itemconfig(coord, fill='red')
            return True

        return False

    def skicka(self, data, gui):
        data = str(data).encode('utf-8')
        try:
            self.conn.send(data)
        except:
            try:
                self.server.sendall(data)
            except:
                gui.start()
                return

        if data == b'redo':
            self.p1_starta = True

            if hasattr(self, 'p2_starta'):
                print('båda är anslutna!!!')
                gui.redo.pack_forget()
                gui.spela()
