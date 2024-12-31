import tkinter as tk
from tkinter import ttk

def gui_process(queue):
    # Initiale Werte für Position und Größe
    cubes = [{"position": [0, 0, 0], "size": [1, 1, 1], "color": "red"}]

    cube_position = [0, 0, 0]
    cube_size = [1, 1, 1]

    def quit_program():
        print("Programm wird beendet...")
        queue.put("QUIT")  # Sende Beenden-Befehl an die Queue
        root.quit()  # Schließt das GUI-Fenster
        root.destroy()  # Beendet den Tkinter-Thread



    def send_update():
        # Sende die aktuellen Werte an die Queue
        queue.put({
            "position": [
                int(pos_x_slider.get()),
                int(pos_y_slider.get()),
                int(pos_z_slider.get())
            ],
            "size": [
                int(size_x_slider.get()),
                int(size_y_slider.get()),
                int(size_z_slider.get())
            ]
        })

    # Tkinter-GUI erstellen
    root = tk.Tk()
    root.title("3D Cube Controller")
    root.geometry("400x400+800+100")  # Größe und Position (400x400 Pixel, 100px von oben/links)


    # Menüleiste erstellen
    menu_bar = tk.Menu(root)
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Beenden", command=quit_program)  # Beenden-Option
    menu_bar.add_cascade(label="Datei", menu=file_menu)
    root.config(menu=menu_bar)  # Menüleiste hinzufügen

    # Positionseinstellungen
    tk.Label(root, text="Position X").pack()
    pos_x_slider = ttk.Scale(root, from_=0, to=10, orient="horizontal")
    pos_x_slider.set(cube_position[0])
    pos_x_slider.pack()

    tk.Label(root, text="Position Y").pack()
    pos_y_slider = ttk.Scale(root, from_=0, to=10, orient="horizontal")
    pos_y_slider.set(cube_position[1])
    pos_y_slider.pack()

    tk.Label(root, text="Position Z").pack()
    pos_z_slider = ttk.Scale(root, from_=0, to=10, orient="horizontal")
    pos_z_slider.set(cube_position[2])
    pos_z_slider.pack()

    # Größeneinstellungen
    tk.Label(root, text="Größe X").pack()
    size_x_slider = ttk.Scale(root, from_=1, to=5, orient="horizontal")
    size_x_slider.set(cube_size[0])
    size_x_slider.pack()

    tk.Label(root, text="Größe Y").pack()
    size_y_slider = ttk.Scale(root, from_=1, to=5, orient="horizontal")
    size_y_slider.set(cube_size[1])
    size_y_slider.pack()

    tk.Label(root, text="Größe Z").pack()
    size_z_slider = ttk.Scale(root, from_=1, to=5, orient="horizontal")
    size_z_slider.set(cube_size[2])
    size_z_slider.pack()

    # Plot-Button
    plot_button = ttk.Button(root, text="Neu plotten", command=send_update)
    plot_button.pack()

    # Tkinter-Loop starten
    root.mainloop()
