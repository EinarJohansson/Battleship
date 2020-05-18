import socket


class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostbyname(socket.getfqdn())
        self.port = 4444
        self.skepp = list()

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
                gui.din_tur()
                

        elif 'träff' in data_str or 'miss' in data_str:
            # kolla om gissningen träffade eller missade
            print(data_str)
            print('vi träffade eller missade!')

            # få fram koordinaten och reslutatet från strängen
            coord, resultat = data_str.split(': ')

            print('koordinaten: ', coord)
            print('resultat: ', resultat)

            coord = eval(coord)

            if resultat == 'träff':
                gui.p2.itemconfig(coord, fill='blue')
            else:
                # Sluta gissa
                gui.p2.itemconfig(coord, fill=gui.red)
                gui.din_tur()
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
                # vår tur att gissa
                gui.min_tur()

    def träff(self, coord, gui):
        # Gör om sträng till tupel
        coord = eval(coord)

        # Kolla om koordinaten har träffat ett av våra skepp
        if coord in self.skepp:
            # rita på våran spelplan att vår motsåndare gisassde rätt på koordinaten
            gui.p1.itemconfig(coord, fill=gui.red)
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
                # Jag börjar att gissa
                gui.min_tur()