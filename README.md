# Battleship
Spela sänka skepp med en kompis på ditt nätverk! 

## Installering
För att hämta koden, kör: 
```bash
git clone https://github.com/EinarJohansson/Battleship.git
```
## Starta ett spel
För att starta ett spel, navigera till installations directoryn och kör:
```bash
python3 main.py
```

## Hur spelar man?
Om du vill ändra riktning skeppet du ska placera, klicka på vilken tangent som helst. 
Sedan klickar du på en ruta som du vill att ditt skepp ska befinna sig på. 

Om du gissar rätt en gång så får du gissa igen.

Om du gissar fel är det din motståndares tur att gissa.

## Felhantering
Om din server adress är 127.0.0.1 så kan inte din kompis ansluta till servern. För att lösa detta, öppna en terminal och skriv:
```bash
ipconfig
```
eller 
```bash
ifconfig
```
om du använder osx/linux. Sedan letar du efter din ipv4 adress som du anväder på ditt nätverk.

