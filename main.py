from multiprocessing import Process, Queue, Manager
from gui_controller import gui_process
from plotter import plot_process

if __name__ == "__main__":
    # Shared Queue erstellen
    queue = Queue()
    manager = Manager()
    
    # Geteilte Cube-Liste erstellen
    cubes = manager.list()  # Geteilte Liste
    cubes.append({"position": [0, 0, 0], "size": [9, 10, 11], "color": "blue", "visible": True})


    # Plot-Prozess starten
    plot_proc = Process(target=plot_process, args=(queue,cubes,))
    plot_proc.start()

    try:
        # GUI-Prozess starten
        gui_process(queue,cubes)
    finally:
        # Sicherstellen, dass der Plot-Prozess beendet wird
        print("Beende den Plot-Prozess...")
        plot_proc.terminate()
        plot_proc.join()
        print("Anwendung wurde vollständig beendet.")