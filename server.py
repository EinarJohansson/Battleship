import socket


class Server:
    def __init__(self):
        # Server inställningar
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostbyname(socket.getfqdn())
        self.port = 4444

        # Håll koll på skeppen och om spelet är över eller inte
        self.fortsätt = True
        self.skepp = set()
        self.träffade = set()

    def lyssna(self, gui):
        '''Lyssna efter inkommande data från vår motståndare'''
        with self.server as s:
            try:
                s.bind((self.host, self.port))
                s.listen()
            except:
                gui.start()
                return

            # Ta emot ett connection objekt och vår motståndares adress
            self.conn, self.addr = s.accept()

            with self.conn:
                print('Connected by', self.addr)
                # Gå vidare till att starta spelet
                gui.placera_skepp()

                # Ta emot data
                while True:
                    if not self.fortsätt:
                        break
                    data = self.conn.recv(1024)

                    if data:
                        self.hantera(data, gui)
                    else:
                        self.stäng(gui)
                        break

    def anslut(self, gui, host):
        '''Anslut till vår motståndares server'''
        with self.server as s:
            try:
                s.connect((host, 4444))
            except:
                gui.start()
                return

            # Starta spelet
            gui.placera_skepp()

            # Ta emot data
            while True:
                if not self.fortsätt:
                    break
                data = s.recv(1024)
                if data:
                    self.hantera(data, gui)
                else:
                    self.stäng(gui)
                    break

    def hantera(self, data, gui):
        '''Hantera datat vi har tagit emot'''
        data_str = str(data.decode('utf-8')).strip()

        if data_str == 'redo':
            self.p2_starta = True
            if hasattr(self, 'p1_starta') and hasattr(self, 'p2_starta'):
                # Båda är anslutna!
                gui.redo.pack_forget()
                gui.din_tur()
        elif 'träff' in data_str or 'miss' in data_str or 'vinst' in data_str:
            # kolla om gissningen träffade eller missade

            # få fram koordinaten och reslutatet från strängen
            coord, resultat = data_str.split(': ')

            print('koordinaten: ', coord)
            print('resultat: ', resultat)

            # Konvertera datatyp från sträng till tippel
            coord = eval(coord)

            if resultat == 'träff':
                gui.p2.itemconfig(coord, fill='blue')
            elif resultat == 'vinst':
                # Vi har vunnit!
                gui.p2.itemconfig(coord, fill='blue')
                gui.resultat('vann')
            else:
                # Sluta gissa
                gui.p2.itemconfig(coord, fill=gui.red)
                gui.din_tur()
        else:
            # inkommande koordinater, kolla om det är miss eller träff

            if self.träff(data_str, gui) == 'förlust':
                # Skicka att vår motståndare vann
                svar = str(data_str + ': vinst')
                self.skicka(svar, gui)
                gui.resultat('förlora')
            elif self.träff(data_str, gui):
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
        '''Kolla om vår motståndare har träffat vårt skepp'''
        # Gör om sträng till tupel
        coord = eval(coord)

        # Kolla om koordinaten har träffat ett av våra skepp
        if coord in self.skepp:
            # rita på våran spelplan att vår motsåndare gisassde rätt på koordinaten
            gui.p1.itemconfig(coord, fill=gui.red)

            # Spara att koordinaten har blivit träffad
            self.träffade.add(coord)

            if self.skepp == self.träffade:
                # Vi förlorade
                return 'förlust'
            
            return True

        return False

    def skicka(self, data, gui):
        '''Skicka data till vår motståndare'''
        data = str(data).encode('utf-8')
        try:
            self.conn.send(data)
        except:
            try:
                self.server.sendall(data)
            except:
                self.stäng(gui)
                return

        if data == b'redo':
            self.p1_starta = True

            if hasattr(self, 'p2_starta'):
                print('båda är anslutna!!!')
                gui.redo.pack_forget()
                # Jag börjar att gissa
                gui.min_tur()

    def stäng(self, gui):
        '''Stäng ner vår anslutning''' 
        gui.start()
        try:
            self.conn.close()
        except Exception as e:
            print(e)
            
        self.fortsätt = False