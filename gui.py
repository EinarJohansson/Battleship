import tkinter as tk
from tkinter import font
import socket
from server import Server
import threading


class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Sänka skepp')
        self.window.geometry('1000x700')
        self.blue = '#142a43'
        self.green = '#9cffba'

        self.window.configure(bg=self.blue)
        self.host = socket.gethostbyname(socket.getfqdn())
        self.öra = Server()
        self.start()

    def start(self):
        self.clear()

        titel = tk.Label(self.window, text='Sänka skepp',
                         bg=self.blue, fg=, font=('Roboto', 70))
        b_skapa = tk.Button(self.window, text='Skapa server', height=2, width=20, font=(
            'Roboto', 20), command=self.skapa)
        b_anslut = tk.Button(self.window, text='Anslut till server',
                             height=2, width=20, font=('Roboto', 20), command=self.anslut)

        titel.pack(pady=50)
        b_skapa.pack(pady=10)
        b_anslut.pack(pady=30)

    def skapa(self):
        self.clear()

        if not hasattr(self, 'tråd'):
            tråd = threading.Thread(target=self.öra.lyssna, args=(self,))
            tråd.start()

        titel = tk.Label(self.window, text='Sänka skepp',
                         bg=self.blue, fg=self.green, font=('Roboto', 70))
        info = tk.Label(self.window, text='Väntar på att någon ska ansluta till din server...',
                        bg=self.blue, fg='grey', font=('Roboto', 20))
        uuid = tk.Label(self.window, text=self.host,
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
        self.clear()

        titel = tk.Label(self.window, text='Sänka skepp',
                         bg=self.blue, fg=self.green, font=('Roboto', 70))

        adress = tk.Entry(self.window, width=50)

        b_anslut = tk.Button(self.window, text='Anslut',
                            height=2, width=20, font=('Roboto', 20),
                            command=lambda: threading.Thread(target=self.öra.anslut,
                            args=(self, adress.get(),)).start())

        b_avbryt = tk.Button(self.window, text='Avbryt', height=2, width=20, font=(
            'Roboto', 20), command=self.start)

        titel.pack(pady=50)
        adress.pack(pady=10)
        b_anslut.pack(pady=30)
        b_avbryt.pack(pady=10)

    def placera_skepp(self):
        self.clear()

        titel = tk.Label(self.window, text='Sänka skepp',
                         bg=self.blue, fg=self.green, font=('Roboto', 70))

        self.p1 = tk.Canvas(self.window, width=400, height=400, bg=self.blue)

        self.p2 = tk.Canvas(self.window, width=400, height=400, bg=self.blue)

        self.redo = tk.Button(self.window, text='Redo', height=2, width=20, font=(
            'Roboto', 20), command=lambda: self.öra.redo(self))

        titel.pack()
        self.p1.pack(side=tk.LEFT, padx=50)
        self.redo.pack(side=tk.LEFT, expand=tk.YES)
        self.p2.pack(side=tk.RIGHT, padx=50)

        for r in range(10):
            for c in range(10):
                coords = (c*20, r*20, c*20+20, r*20+20)
                # Din spelplan
                self.p1.create_rectangle(coords, fill=self.blue, width=2)
                # Fiendens spelplan
                self.p2.create_rectangle(coords, fill=self.blue, width=2)

        self.p1.bind('<Button-1>', lambda event: self.p1.itemconfig(tk.CURRENT, fill=self.green))

    def spela(self):
        self.p1.unbind('<Button-1>')
        self.p2.bind('<Button-1>', lambda event: self.gissa(event))

    def gissa(self, event):
        coord = event.widget.find_withtag(tk.CURRENT)

        # Skicka koordinaten till motståndarens server och kolla om den är träffad eller inte
        self.öra.gissa(self, coord)

        #träff = self.p2.itemcget(coord, 'fill')

    def kopiera(self):
        self.window.clipboard_clear()
        self.window.clipboard_append(self.host)

    def clear(self):
        # Clear window
        children = self.window.winfo_children()
        for child in children:
            child.destroy()
