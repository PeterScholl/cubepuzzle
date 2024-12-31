import tkinter as tk
from tkinter import ttk
from tkinter.colorchooser import askcolor  # Für Farbauswahl

def gui_process(queue):
    # Initiale Werte für Position und Größe
    cubes = [{"position": [0, 0, 0], "size": [1, 1, 1], "color": "red"}]

    def update_gui_fields():
        """Aktualisiere die GUI-Felder basierend auf dem ausgewählten Cube."""
        index = selected_cube_index.get()
        pos = cubes[index]["position"]
        size = cubes[index]["size"]
        color_label.config(text=cubes[index]["color"], bg=cubes[index]["color"])
        pos_x_slider.set(pos[0])
        pos_y_slider.set(pos[1])
        pos_z_slider.set(pos[2])
        size_x_slider.set(size[0])
        size_y_slider.set(size[1])
        size_z_slider.set(size[2])

    def quit_program():
        print("Programm wird beendet...")
        queue.put("QUIT")  # Sende Beenden-Befehl an die Queue
        root.quit()  # Schließt das GUI-Fenster
        root.destroy()  # Beendet den Tkinter-Thread



    def send_update():
        """Sende die aktuellen Werte des ausgewählten Cubes an die Queue."""
        index = selected_cube_index.get()
        cubes[index]["position"] = [
            int(pos_x_slider.get()),
            int(pos_y_slider.get()),
            int(pos_z_slider.get()),
        ]
        cubes[index]["size"] = [
            int(size_x_slider.get()),
            int(size_y_slider.get()),
            int(size_z_slider.get()),
        ]
        data = {"index": index, **cubes[index]}
        print(f"Sende folgende Daten: {data}")  # Debug-Ausgabe
        queue.put(data)

    def add_cube():
        """Füge einen neuen Cube hinzu."""
        cubes.append({"position": [0, 0, 0], "size": [1, 1, 1], "color": "red"})
        cube_selector["menu"].add_command(label=f"Cube {len(cubes) - 1}", command=lambda idx=len(cubes) - 1: select_cube(idx))
        print(f"Neuer Cube hinzugefügt. Gesamtzahl: {len(cubes)}")

    def delete_cube():
        """Lösche den aktuell ausgewählten Cube."""
        index = selected_cube_index.get()
        if len(cubes) > 1:
            del cubes[index]
            selected_cube_index.set(0)  # Wähle den ersten Cube
            update_cube_selector()
            update_gui_fields()
            print(f"Cube {index} gelöscht. Verbleibende Cubes: {len(cubes)}")

    def select_cube(index):
        """Wähle einen Cube aus der Liste."""
        selected_cube_index.set(index)
        update_gui_fields()

    def update_cube_selector():
        """Aktualisiere die Cube-Auswahlliste."""
        cube_selector["menu"].delete(0, "end")  # Lösche alle bisherigen Einträge
        for idx, cube in enumerate(cubes):
            # Füge jeden Cube mit seinem Index hinzu
            cube_selector["menu"].add_command(
                label=f"Cube {idx}",  # Anzeigename
                command=lambda idx=idx: select_cube(idx)  # Tatsächlicher Wert
            )
            
    def choose_color():
        """Öffne einen Farbauswahldialog."""
        index = selected_cube_index.get()
        color_code, rgb = askcolor(title="Wähle eine Farbe")
        if color_code:
            # Umwandlung von RGB-Tupel zu Hex-String
            #hex_color = "#{:02x}{:02x}{:02x}".format(int(rgb[0]), int(rgb[1]), int(rgb[2]))
            hex_color = rgb
            # Setze die neue Farbe für den Cube
            cubes[index]["color"] = hex_color
            color_label.config(text=hex_color, bg=hex_color)
            
            # Werte an die Queue senden
            send_update()



    # Tkinter-GUI erstellen
    root = tk.Tk()
    root.title("3D Cube Controller")
    root.geometry("400x400+800+100")  # Größe und Position (400x400 Pixel, 100px von oben/links)
    selected_cube_index = tk.IntVar(value=0)  # Index des aktuell ausgewählten Cubes


    # Menüleiste erstellen
    menu_bar = tk.Menu(root)
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Beenden", command=quit_program)  # Beenden-Option
    menu_bar.add_cascade(label="Datei", menu=file_menu)
    root.config(menu=menu_bar)  # Menüleiste hinzufügen

    # Dropdown-Menü zur Cube-Auswahl
    tk.Label(root, text="Wähle einen Cube:").pack()
    # Erstelle das OptionMenu mit den Indizes (Integer) als Werte
    cube_selector = tk.OptionMenu(
        root,
        selected_cube_index,
        *range(len(cubes)),  # Werte sind die Indizes der Cubes
        command=select_cube
    )
    cube_selector.pack()

    # Positionseinstellungen
    tk.Label(root, text="Position X").pack()
    pos_x_slider = ttk.Scale(root, from_=0, to=10, orient="horizontal", command=lambda _: send_update())
    pos_x_slider.pack()

    tk.Label(root, text="Position Y").pack()
    pos_y_slider = ttk.Scale(root, from_=0, to=10, orient="horizontal", command=lambda _: send_update())
    pos_y_slider.pack()

    tk.Label(root, text="Position Z").pack()
    pos_z_slider = ttk.Scale(root, from_=0, to=10, orient="horizontal", command=lambda _: send_update())
    pos_z_slider.pack()

    # Größeneinstellungen
    tk.Label(root, text="Größe X").pack()
    size_x_slider = ttk.Scale(root, from_=1, to=5, orient="horizontal", command=lambda _: send_update())
    size_x_slider.pack()

    tk.Label(root, text="Größe Y").pack()
    size_y_slider = ttk.Scale(root, from_=1, to=5, orient="horizontal", command=lambda _: send_update())
    size_y_slider.pack()

    tk.Label(root, text="Größe Z").pack()
    size_z_slider = ttk.Scale(root, from_=1, to=5, orient="horizontal", command=lambda _: send_update())
    size_z_slider.pack()

    # Farbauswahl
    tk.Label(root, text="Farbe:").pack()
    color_label = tk.Label(root, text="red", bg="red", width=10)
    color_label.pack()
    color_button = ttk.Button(root, text="Farbe wählen", command=choose_color)
    color_button.pack()

    # Buttons zum Hinzufügen/Löschen von Cubes
    ttk.Button(root, text="Neuen Cube hinzufügen", command=add_cube).pack()
    ttk.Button(root, text="Ausgewählten Cube löschen", command=delete_cube).pack()

    # Felder initialisieren
    update_gui_fields()

    # Tkinter-Loop starten
    root.mainloop()
