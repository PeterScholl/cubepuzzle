from multiprocessing import Process, Queue
from gui_controller import gui_process
from plotter import plot_process

if __name__ == "__main__":
    # Shared Queue erstellen
    queue = Queue()

    # Plot-Prozess starten
    plot_proc = Process(target=plot_process, args=(queue,))
    plot_proc.start()

    try:
        # GUI-Prozess starten
        gui_process(queue)
    finally:
        # Sicherstellen, dass der Plot-Prozess beendet wird
        print("Beende den Plot-Prozess...")
        plot_proc.terminate()
        plot_proc.join()
        print("Anwendung wurde vollständig beendet.")