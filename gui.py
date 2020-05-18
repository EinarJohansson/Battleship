import tkinter as tk
from tkinter import font
import socket
from server import Server
import threading


class GUI:
    def __init__(self):
        # Guins färgschema
        self.blue = '#142a43'
        self.green = '#9cffba'
        self.red = '#FF0000'
        
        # Fönstrets inställningar
        self.window = tk.Tk()
        self.window.title('Sänka skepp')
        self.window.geometry('1000x700')
        self.window.configure(bg=self.blue)

        # Servern
        self.öra = Server()
        
        # Gå till startsidan
        self.start()

    def start(self):
        '''Programmets startsida'''

        self.clear()

        titel = tk.Label(self.window, text='Sänka skepp', bg=self.blue, fg=self.green, font=('Roboto', 70))
        b_skapa = tk.Button(self.window, text='Skapa server', height=2, width=20, font=(
            'Roboto', 20), command=self.skapa)
        b_anslut = tk.Button(self.window, text='Anslut till server',
                             height=2, width=20, font=('Roboto', 20), command=self.anslut)

        titel.pack(pady=50)
        b_skapa.pack(pady=10)
        b_anslut.pack(pady=30)

    def skapa(self):
        '''GUI för att skapa en server'''
        self.clear()

        if not hasattr(self, 'lyssna_tråd'):
            self.lyssna_tråd = threading.Thread(target=self.öra.lyssna, args=(self,))
            self.lyssna_tråd.start()

        titel = tk.Label(self.window, text='Sänka skepp',
                         bg=self.blue, fg=self.green, font=('Roboto', 70))
        info = tk.Label(self.window, text='Väntar på att någon ska ansluta till din server...',
                        bg=self.blue, fg='grey', font=('Roboto', 20))
        uuid = tk.Label(self.window, text=self.öra.host,
                        bg=self.blue, fg='white', font=('Roboto', 20))

        f = font.Font(uuid, uuid.cget('font'))
        f.configure(underline=True)
        uuid.configure(font=f)

        b_kopiera = tk.Button(self.window, text='Kopiera Server IP',
                              height=2, width=20, font=('Roboto', 20), command=self.kopiera)
        b_avbryt = tk.Button(self.window, text='Avbryt', height=2, width=20, font=(
            'Roboto', 20), command=self.start)

        titel.pack(pady=50)
        uuid.pack()
        info.pack(pady=10)
        b_kopiera.pack(pady=30)
        b_avbryt.pack(pady=10)

    def anslut(self):
        '''GUI för att ansluta till en server'''
        self.clear()

        titel = tk.Label(self.window, text='Sänka skepp',
                         bg=self.blue, fg=self.green, font=('Roboto', 70))

        adress = tk.Entry(self.window, width=50)

        b_anslut = tk.Button(self.window, text='Anslut',
                            height=2, width=20, font=('Roboto', 20),
                            command=lambda: self.skapa_tråd(adress.get()))

        b_avbryt = tk.Button(self.window, text='Avbryt', height=2, width=20, font=(
            'Roboto', 20), command=self.start)

        titel.pack(pady=50)
        adress.pack(pady=10)
        b_anslut.pack(pady=30)
        b_avbryt.pack(pady=10)

    def skapa_tråd(self, adress):
        if not hasattr(self, 'anslut_tråd'):
            self.anslut_tråd = threading.Thread(target=self.öra.anslut, args=(self, adress,))
            self.anslut_tråd.start()

    def placera_skepp(self):
        '''GUI för att placera ut sina skepp'''
        self.clear()

        titel = tk.Label(self.window, text='Sänka skepp',
                         bg=self.blue, fg=self.green, font=('Roboto', 70))

        self.p1 = tk.Canvas(self.window, width=400, height=400, bg=self.blue)

        self.p2 = tk.Canvas(self.window, width=400, height=400, bg=self.blue)

        self.redo = tk.Button(self.window, text='Redo', height=2, width=20, font=(
            'Roboto', 20), command=lambda: self.öra.skicka('redo', self))

        titel.pack()
        self.p1.pack(side=tk.LEFT, padx=50)
        self.redo.pack(side=tk.LEFT, expand=tk.YES)
        self.p2.pack(side=tk.RIGHT, padx=50)

        for r in range(10):
            for c in range(10):
                coords = (c*40, r*40, c*40+40, r*40+40)
                # Min spelplan
                self.p1.create_rectangle(coords, fill=self.blue, width=2)
                # Din spelplan
                self.p2.create_rectangle(coords, fill=self.blue, width=2)        
        
        self.p1.bind('<Button-1>', lambda event: self.spara_skepp(event))
    
    def spara_skepp(self, event):
        '''Spara skeppens koordinater i server klassen'''
        
        # Hämta skeppets koordinat
        coord = event.widget.find_withtag(tk.CURRENT)
        self.öra.skepp.add(coord)

        # Rita skeppet
        self.p1.itemconfig(tk.CURRENT, fill=self.green)

    def min_tur(self):
        '''Min tur att gissa'''
        self.p1.unbind('<Button-1>')
        self.p2.bind('<Button-1>', lambda event: self.gissa(event))
    
    def din_tur(self):
        '''Din tur att gissa'''
        self.p1.unbind('<Button-1>')
        self.p2.unbind('<Button-1>')

    def gissa(self, event):
        '''Kolla med servern om vår gissning är korrekt eller inte''' 
        coord = event.widget.find_withtag(tk.CURRENT)

        # Skicka koordinaten till motståndarens server och kolla om den är träffad eller inte
        self.öra.skicka(coord, self)

    def kopiera(self):
        '''Kopiera servernamnet så att man enkelt kan dela hostnamnet med en kompis'''
        self.window.clipboard_clear()
        self.window.clipboard_append(self.öra.host)

    def clear(self):
        '''Rensa rutan från onödigt mojs'''
        children = self.window.winfo_children()
        for child in children:
            child.destroy()

    def resultat(self, resultat):
        '''Visa att vi vann/förlora'''        
        self.clear()

        self.öra.fortsätt = False

        text = tk.Label(self.window, text=f'Du {resultat}!',
                        bg=self.blue, fg=self.green, font=('Roboto', 70))
        start = tk.Button(self.window, text='Gå till startskärm', height=2, width=20, font=(
            'Roboto', 20), command=self.start)
        
        text.pack()
        start.pack()