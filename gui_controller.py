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
        update_cube_selector()
        selected_cube_index.set(len(cubes) - 1)  # Wähle den neuen Cube aus
        update_gui_fields()
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

    # Frames erstellen
    top_frame = tk.Frame(root) #Für Cube auswahl
    top_frame.pack(fill="x", pady=5)

    middle_frame = tk.Frame(root) #Für die Slider
    middle_frame.pack(fill="both", expand=True, pady=5)

    bottom_frame = tk.Frame(root) #Für Farbauswahl und Buttons
    bottom_frame.pack(fill="x", pady=5)

    # Cube-Auswahl im oberen Frame
    tk.Label(top_frame, text="Wähle einen Cube:").pack(side="left", padx=5)
    cube_selector = tk.OptionMenu(
        top_frame,
        selected_cube_index,
        *range(len(cubes)),
        command=select_cube
    )
    cube_selector.pack(side="left", padx=5)
    update_cube_selector()

    # Grid-Layout für Schieberegler im mittleren Frame
    minpos=0
    maxpos=30
    minsize=9
    maxsize=11
    # Grid für Position X
    tk.Label(middle_frame, text="Position X").grid(row=0, column=0, sticky="w", padx=5, pady=2)
    pos_x_slider = ttk.Scale(middle_frame, from_=minpos, to=maxpos, orient="horizontal", command=lambda val: (pos_x_value_label.config(text=f"{int(float(val))}"), send_update()))
    pos_x_slider.grid(row=0, column=1, sticky="we", padx=5, pady=2)  # Schieberegler füllt horizontal
    pos_x_value_label = tk.Label(middle_frame, text="0", width=5)
    pos_x_value_label.grid(row=0, column=2, sticky="e", padx=5, pady=2)

    # Grid für Position Y
    tk.Label(middle_frame, text="Position Y").grid(row=1, column=0, sticky="w", padx=5, pady=2)
    pos_y_slider = ttk.Scale(middle_frame, from_=minpos, to=maxpos, orient="horizontal", command=lambda val: (pos_y_value_label.config(text=f"{int(float(val))}"), send_update()))
    pos_y_slider.grid(row=1, column=1, sticky="we", padx=5, pady=2)
    pos_y_value_label = tk.Label(middle_frame, text="0", width=5)
    pos_y_value_label.grid(row=1, column=2, sticky="e", padx=5, pady=2)

    # Grid für Position Z
    tk.Label(middle_frame, text="Position Z").grid(row=2, column=0, sticky="w", padx=5, pady=2)
    pos_z_slider = ttk.Scale(middle_frame, from_=minpos, to=maxpos, orient="horizontal", command=lambda val: (pos_z_value_label.config(text=f"{int(float(val))}"), send_update()))
    pos_z_slider.grid(row=2, column=1, sticky="we", padx=5, pady=2)
    pos_z_value_label = tk.Label(middle_frame, text="0", width=5)
    pos_z_value_label.grid(row=2, column=2, sticky="e", padx=5, pady=2)

    # Grid für Größe X
    tk.Label(middle_frame, text="Größe X").grid(row=3, column=0, sticky="w", padx=5, pady=2)
    size_x_slider = tk.Scale(middle_frame, from_=minsize, to=maxsize, orient="horizontal",
                             resolution=1,
                             command=lambda val: (size_x_value_label.config(text=f"{int(float(val))}"), send_update()))
    size_x_slider.grid(row=3, column=1, sticky="we", padx=5, pady=2)
    size_x_value_label = tk.Label(middle_frame, text="9", width=5)
    size_x_value_label.grid(row=3, column=2, sticky="e", padx=5, pady=2)

    # Grid für Größe Y
    tk.Label(middle_frame, text="Größe Y").grid(row=4, column=0, sticky="w", padx=5, pady=2)
    size_y_slider = tk.Scale(middle_frame, from_=minsize, to=maxsize, orient="horizontal",
                             resolution = 1,
                             command=lambda val: (size_y_value_label.config(text=f"{int(float(val))}"), send_update()))
    size_y_slider.grid(row=4, column=1, sticky="we", padx=5, pady=2)
    size_y_value_label = tk.Label(middle_frame, text="9", width=5)
    size_y_value_label.grid(row=4, column=2, sticky="e", padx=5, pady=2)

    # Grid für Größe Z
    tk.Label(middle_frame, text="Größe Z").grid(row=5, column=0, sticky="w", padx=5, pady=2)
    size_z_slider = tk.Scale(middle_frame, from_=minsize, to=maxsize, orient="horizontal",
                             resolution = 1,
                              command=lambda val: (size_z_value_label.config(text=f"{int(float(val))}"), send_update()))
    size_z_slider.grid(row=5, column=1, sticky="we", padx=5, pady=2)
    size_z_value_label = tk.Label(middle_frame, text="9", width=5)
    size_z_value_label.grid(row=5, column=2, sticky="e", padx=5, pady=2)


    # Farbauswahl und Buttons im Grid-Layout (bottom_frame)
    # Farbe und Farbfeld in einer Zelle
    color_frame = tk.Frame(bottom_frame)
    color_frame.grid(row=0, column=0, columnspan=1, sticky="w", padx=5, pady=2)

    tk.Label(color_frame, text="Farbe:").pack(side="left", padx=5)
    color_label = tk.Label(color_frame, text="red", bg="red", width=10)
    color_label.pack(side="left", padx=5)

    color_button = ttk.Button(bottom_frame, text="Farbe wählen", command=choose_color)
    color_button.grid(row=0, column=1, padx=5, pady=2, sticky="we")

    # Buttons
    add_cube_button = ttk.Button(bottom_frame, text="Neuen Cube hinzufügen", command=add_cube)
    add_cube_button.grid(row=1, column=0, padx=5, pady=2, sticky="we")

    delete_cube_button = ttk.Button(bottom_frame, text="Ausgewählten Cube löschen", command=delete_cube)
    delete_cube_button.grid(row=1, column=1, padx=5, pady=2, sticky="we")
    
    bottom_frame.grid_columnconfigure(0, weight=1)
    bottom_frame.grid_columnconfigure(1, weight=1)
    bottom_frame.grid_columnconfigure(2, weight=1)



    # Felder initialisieren
    update_gui_fields()

    # Tkinter-Loop starten
    root.mainloop()
