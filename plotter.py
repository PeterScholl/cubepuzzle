import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def plot_process(queue):
    print("Plot-Prozess gestartet...")

    # Funktion zum Zeichnen eines Quaders
    def draw_cube(ax, position, size, color='blue', alpha=0.7):
        x, y, z = position
        dx, dy, dz = size

        # Vertices des Quaders
        vertices = [
            [x, y, z],
            [x + dx, y, z],
            [x + dx, y + dy, z],
            [x, y + dy, z],
            [x, y, z + dz],
            [x + dx, y, z + dz],
            [x + dx, y + dy, z + dz],
            [x, y + dy, z + dz],
        ]

        # Flächen des Quaders
        faces = [
            [vertices[0], vertices[1], vertices[5], vertices[4]],  # Boden
            [vertices[2], vertices[3], vertices[7], vertices[6]],  # Deckel
            [vertices[0], vertices[4], vertices[7], vertices[3]],  # Seite vorne
            [vertices[1], vertices[5], vertices[6], vertices[2]],  # Seite hinten
            [vertices[0], vertices[1], vertices[2], vertices[3]],  # Seite links
            [vertices[4], vertices[5], vertices[6], vertices[7]],  # Seite rechts
        ]

        ax.add_collection3d(Poly3DCollection(faces, facecolors=color, linewidths=1, edgecolors='black', alpha=alpha))

    # Matplotlib-Plot initialisieren
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Initialer Quader
    cube_position = [0, 0, 0]
    cube_size = [1, 1, 1]

    # Funktion zum Replotten
    def replot():
        ax.clear()  # Lösche den alten Plot
        draw_cube(ax, tuple(cube_position), tuple(cube_size), color='red')
        ax.set_xlim([0, 10])
        ax.set_ylim([0, 10])
        ax.set_zlim([0, 10])
        ax.set_xlabel('X-Achse')
        ax.set_ylabel('Y-Achse')
        ax.set_zlabel('Z-Achse')
        plt.draw()

    # Interaktiver Plot
    plt.ion()
    replot()
    plt.show()

    # Empfange Daten von der Queue und aktualisiere den Plot
    while True:
        if not queue.empty():
            # Debug: Daten aus der Queue abrufen
            print("Daten in der Queue erkannt. Aktualisiere den Plot...")
            command = queue.get()
            if command == "QUIT":
                print("Beenden-Befehl empfangen. Schließe das Plot-Fenster...")
                plt.close()  # Schließe das Plot-Fenster
                break        # Beende die Schleife
            else:
                print(f"Empfangene Daten: {command}")
                cube_position = command["position"]
                cube_size = command["size"]
                replot()
        else:
            # Debug: Keine neuen Daten
            #print("Keine neuen Daten in der Queue. Warte...")
            plt.pause(0.1)  # CPU-Last reduzieren

