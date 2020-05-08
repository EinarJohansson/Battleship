import tkinter as tk
from tkinter import font
import socket
from server import Server
import threading

class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Sänka skepp")
        self.window.geometry("800x700")
        self.window.configure(bg="#142a43")
        self.host = socket.gethostbyname(socket.getfqdn())
        self.start()

    def start(self):
        self.clear() 

        titel = tk.Label(self.window, text="Sänka skepp", bg="#142a43", fg="#9cffba", font=("Roboto", 70))
        b_skapa = tk.Button(self.window, text="Skapa server", height=2, width=20, font=("Roboto", 20), command=self.skapa)
        b_anslut = tk.Button(self.window, text="Anslut till server", height=2, width=20, font=("Roboto", 20), command=self.anslut)

        titel.pack(pady=50)
        b_skapa.pack(pady=10)
        b_anslut.pack(pady=30)
    
    def skapa(self):
        self.clear()

        if not hasattr(self, 'öra'):
            self.öra = Server()
            tråd = threading.Thread(target=self.öra.lyssna, args=(self,))
            tråd.start()

        titel = tk.Label(self.window, text="Sänka skepp", bg="#142a43", fg="#9cffba", font=("Roboto", 70))
        info = tk.Label(self.window, text="Väntar på att någon ska ansluta till din server...", bg="#142a43", fg="grey", font=("Roboto", 20))
        uuid = tk.Label(self.window, text=self.host, bg="#142a43", fg="white", font=("Roboto", 20))
        
        f = font.Font(uuid, uuid.cget("font"))
        f.configure(underline=True)
        uuid.configure(font=f)

        b_kopiera = tk.Button(self.window, text="Kopiera Server IP", height=2, width=20, font=("Roboto", 20), command=self.kopiera) 
        b_avbryt = tk.Button(self.window, text="Avbryt", height=2, width=20, font=("Roboto", 20), command=self.start) 

        titel.pack(pady=50)
        uuid.pack()
        info.pack(pady=10)
        b_kopiera.pack(pady=30)
        b_avbryt.pack(pady=10)

    def anslut(self):
        self.clear()
        
        titel = tk.Label(self.window, text="Sänka skepp", bg="#142a43", fg="#9cffba", font=("Roboto", 70))
        adress = tk.Entry(self.window, width=50)
        b_anslut = tk.Button(self.window, text="Anslut", height=2, width=20, font=("Roboto", 20))
        b_avbryt = tk.Button(self.window, text="Avbryt", height=2, width=20, font=("Roboto", 20), command=self.start) 
       
        titel.pack(pady=50)
        adress.pack(pady=10)
        b_anslut.pack(pady=30)
        b_avbryt.pack(pady=10)
    
    def spela(self):
        self.clear()

        titel = tk.Label(self.window, text="Sänka skepp", bg="#142a43", fg="#9cffba", font=("Roboto", 70))
        titel.grid(row=0, column=0)
        
        p1 = tk.Canvas(self.window, width=300, height=600)
        p1.grid(row=1, column=0)
        
        p2 = tk.Canvas(self.window, width=300, height=600)
        p2.grid(row=1, column=1)


        # Spelare 1 plan
        for r in range(10):
            for c in range(10):
                coords = (c*30+4, r*30+4, c*30+30, r*30+30)
                p1.create_rectangle(coords, fill='white', width=2)
        
        p1.bind('<Button-1>', lambda event: p1.itemconfig(tk.CURRENT, fill="blue"))


    def kopiera(self):
        self.window.clipboard_clear()
        self.window.clipboard_append(self.host)
    
    def clear(self):
        # Clear window
        children = self.window.winfo_children()
        for child in children:
            child.destroy()