# Importieren der benötigten Module
import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# Erstellen der grafischen Oberfläche
window = tk.Tk()
window.title("Video Overlay")
window.geometry("800x600")

# Erstellen der Widgets
video1_label = tk.Label(window, text="Kein Video 1 ausgewählt")
video1_label.pack()

video2_label = tk.Label(window, text="Kein Video 2 ausgewählt")
video2_label.pack()

overlay_label = tk.Label(window, text="Wähle einen Overlay aus:")
overlay_label.pack()

overlay_var = tk.StringVar(window)
overlay_var.set("Addition")
overlay_menu = tk.OptionMenu(window, overlay_var, "Addition", "Subtraktion", "Multiplikation", "Division", "AND", "OR", "XOR")
overlay_menu.pack()

apply_button = tk.Button(window, text="Overlay anwenden")
apply_button.pack()

save_button = tk.Button(window, text="Video speichern")
save_button.pack()

# Definieren der Funktionen
def select_video1():
    # Öffnen eines Dateiauswahldialogs
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi")])
    if file_path:
        # Laden des Videos mit OpenCV
        global video1
        video1 = cv2.VideoCapture(file_path)
        # Anzeigen des Videonamens
        video1_label.config(text=file_path.split("/")[-1])
        # Aktivieren des Anwenden-Buttons, wenn beide Videos ausgewählt sind
        if video2:
            apply_button.config(state=tk.NORMAL)

def select_video2():
    # Öffnen eines Dateiauswahldialogs
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi")])
    if file_path:
        # Laden des Videos mit OpenCV
        global video2
        video2 = cv2.VideoCapture(file_path)
        # Anzeigen des Videonamens
        video2_label.config(text=file_path.split("/")[-1])
        # Aktivieren des Anwenden-Buttons, wenn beide Videos ausgewählt sind
        if video1:
            apply_button.config(state=tk.NORMAL)

def apply_overlay():
    # Lesen der aktuellen Frames von beiden Videos
    ret1, frame1 = video1.read()
    ret2, frame2 = video2.read()
    if ret1 and ret2:
        # Anpassen der Größe der Frames, damit sie gleich sind
        height, width, _ = frame1.shape
        frame2 = cv2.resize(frame2, (width, height))
        # Anwenden des gewählten Overlays
        overlay_name = overlay_var.get()
        if overlay_name == "Addition":
            frame = cv2.add(frame1, frame2)
        elif overlay_name == "Subtraktion":
            frame = cv2.subtract(frame1, frame2)
        elif overlay_name == "Multiplikation":
            frame = cv2.multiply(frame1, frame2)
        elif overlay_name == "Division":
            frame = cv2.divide(frame1, frame2)
        elif overlay_name == "AND":
            frame = cv2.bitwise_and(frame1, frame2)
        elif overlay_name == "OR":
            frame = cv2.bitwise_or(frame1, frame2)
        elif overlay_name == "XOR":
            frame = cv2.bitwise_xor(frame1, frame2)
        # Erstellen eines neuen Fensters
        global preview_window
        preview_window = tk.Toplevel(window)
        preview_window.title("Vorschau")
        # Erstellen eines neuen Labels in dem Fenster
        global preview_label
        preview_label = tk.Label(preview_window)
        preview_label.pack()
        # Konvertieren des Frames in ein PIL-Image
        image = Image.fromarray(frame)
        # Anzeigen des Frames in dem Fenster
        photo = ImageTk.PhotoImage(image)
        preview_label.config(image=photo)
        preview_label.image = photo
        # Aktivieren des Speichern-Buttons
        save_button.config(state=tk.NORMAL)
    else:
        # Beenden der Videos
        video1.release()
        video2.release()
        overlay_label.config(text="Ende der Videos")

def save_video():
    # Öffnen eines Dateispeicherdialogs
    save_path = filedialog.asksaveasfilename(filetypes=[("Video files", "*.mp4;*.avi")])
    if save_path:
        # Erstellen eines VideoWriter-Objekts
        global writer
        fps = video1.get(cv2.CAP_PROP_FPS)
        width = int(video1.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video1.get(cv2.CAP_PROP_FRAME_HEIGHT))
        writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))
        # Zurückspulen der Videos
        video1.set(cv2.CAP_PROP_POS_FRAMES, 0)
        video2.set(cv2.CAP_PROP_POS_FRAMES, 0)
        # Deaktivieren der Buttons
        apply_button.config(state=tk.DISABLED)
        save_button.config(state=tk.DISABLED)
        # Schließen des Vorschau-Fensters
        preview_window.destroy()
        # Aufrufen der Speicherfunktion
        save_frame()

def save_frame():
    # Lesen der aktuellen Frames von beiden Videos
    ret1, frame1 = video1.read()
    ret2, frame2 = video2.read()
    if ret1 and ret2:
        # Anpassen der Größe der Frames, damit sie gleich sind
        height, width, _ = frame1.shape
        frame2 = cv2.resize(frame2, (width, height))
        # Anwenden des gewählten Overlays
        overlay_name = overlay_var.get()
        if overlay_name == "Addition":
            frame = cv2.add(frame1, frame2)
        elif overlay_name == "Subtraktion":
            frame = cv2.subtract(frame1, frame2)
        elif overlay_name == "Multiplikation":
            frame = cv2.multiply(frame1, frame2)
        elif overlay_name == "Division":
            frame = cv2.divide(frame1, frame2)
        elif overlay_name == "AND":
            frame = cv2.bitwise_and(frame1, frame2)
        elif overlay_name == "OR":
            frame = cv2.bitwise_or(frame1, frame2)
        elif overlay_name == "XOR":
            frame = cv2.bitwise_xor(frame1, frame2)
        # Schreiben des Frames in das VideoWriter-Objekt
        writer.write(frame)
        # Aufrufen der Speicherfunktion erneut
        window.after(10, save_frame)
    else:
        # Beenden der Videos und des VideoWriter-Objekts
        video1.release()
        video2.release()
        writer.release()
        overlay_label.config(text="Video gespeichert")

# Initialisieren der Video-, VideoWriter- und Vorschau-Fenster-Objekts
video1 = None
video2 = None
writer = None
preview_window = None

# Binden der Funktionen an die Buttons
apply_button.config(command=apply_overlay, state=tk.DISABLED)
save_button.config(command=save_video, state=tk.DISABLED)

# Erstellen eines Menüs
menu = tk.Menu(window)
window.config(menu=menu)
file_menu = tk.Menu(menu)
menu.add_cascade(label="Datei", menu=file_menu)
file_menu.add_command(label="Video 1 auswählen", command=select_video1)
file_menu.add_command(label="Video 2 auswählen", command=select_video2)
file_menu.add_command(label="Beenden", command=window.destroy)

# Starten der Hauptschleife
window.mainloop()

