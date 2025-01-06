# kleines Testprogramm zu einem Knobelpuzzle

## Um eine Quaderanordnung mit Quader.py zu suchen folgende Befehle

```
a = QuaderSearchGen()
b = next(a)
b = next(a)
b = next(a)
b = next(a)
saveCubes(generateCubes(qList))
```

erzeugt eine Datei cubes.json, die man im GUI (main.py starten) ansehen kann

![grafik](https://github.com/user-attachments/assets/4ce57bef-7bca-4c08-a3d3-1bc1433e1c46)

## Nebeneffekt - Multiprocessing mit geteilter Queue

Zwei Prozesse die sich eine Queue-Teilen um darüber Nachrichten zu tauschen und auch eine gemeinsame Liste (das war etwas komplexer).
```
from multiprocessing import Process, Queue, Manager
```

## Notizen zur Puzzlelösung
Die Aufgabe besteht darin, 27 Quader, die keine Würfel sind, zu einem größeren Würfel zusammenzubauen (siehe Bild). Dabei haben die Quader die Kantenlängen b-x,b,b+x . Im Programm habe ich b=10 und x=1 gewählt, so dass die Kantenlängen 9,10 und 11 sind.

Der Außenwürfel soll die Kantenlänge 3b haben und hat somit einen Inhalt von 27b³. Man kann nachrechnen, dass die Differenz zum 27fachen Quadervolumen 27bx² beträgt, also z.B. aus 27 Säulen der Grundfläche x² und der Höhe b besteht. In den Lösungen, die der Computer findet, sieht es so aus, als wären in jeder der 9 Ebenen (in jeder Raumrichtung gibt es 3 Ebenen - Senkrecht zur x-Achxe, y-Achse und z-Achse) jeweils 3 von diesen kleinen Säulen als Löcher zu finden sind... Ob das immer so sein muss?

Jedenfalls denke ich ziemlich sicher, dass das Puzzle nur dann lösbar ist, wenn jeder Quader seine Nachbarquader berührt (dieses Ziel strebt die im Programm implementierte Suche an). Ich denke, dass man über das kleinerwerden von x argumentieren kann, bin aber nicht sicher...
