import time
import threading
import tkinter as tk
from tkinter import ttk
import winsound

# -- Constantes par défaut --
DELAI_PAR_DEFAUT = 210  # 3 min 30 sec
DUREE_BIP_PAR_DEFAUT = 5  # secondes
VOLUME_PAR_DEFAUT = 100

class Alarme:
    def __init__(self):
        self.active = False
        self.thread = None
        self.attente = DELAI_PAR_DEFAUT
        self.duree_bip = DUREE_BIP_PAR_DEFAUT
        self.compteur = self.attente
        self.stop_event = threading.Event()

    def boucle_alarme(self):
        self.compteur = self.attente
        while not self.stop_event.is_set():
            while self.compteur > 0 and not self.stop_event.is_set():
                mins, secs = divmod(self.compteur, 60)
                timer_var.set(f"{mins:02}:{secs:02}")
                time.sleep(1)
                self.compteur -= 1
            if self.stop_event.is_set():
                break
            timer_var.set("⏰ Bip ⏰")
            fin = time.time() + self.duree_bip
            while time.time() < fin and not self.stop_event.is_set():
                self.jouer_bip()
                time.sleep(1)
            self.compteur = self.attente
        timer_var.set("Arrêté")

    def jouer_bip(self):
        volume = int(scale_volume.get())
        if volume == 0:
            return  # silence simulé
        winsound.Beep(1000, 500)  # ne gère pas le volume mais code prêt pour autre lib

    def demarrer(self):
        try:
            self.attente = int(entry_attente.get())
            self.duree_bip = int(entry_duree.get())
            self.compteur = self.attente
        except ValueError:
            timer_var.set("Erreur")
            return

        if not self.active:
            self.active = True
            self.stop_event.clear()
            self.thread = threading.Thread(target=self.boucle_alarme, daemon=True)
            self.thread.start()
            timer_var.set("En attente...")

    def arreter(self):
        if self.active:
            self.active = False
            self.stop_event.set()
            self.compteur = self.attente
            timer_var.set("Arrêté")

# -- Interface graphique épurée --
fenetre = tk.Tk()
fenetre.title("Minuteur élégant")
fenetre.geometry("370x320")
fenetre.configure(bg="#f8fafb")

style = ttk.Style()
try:
    fenetre.tk.call('source', 'azure.tcl')
    style.theme_use('azure')
except Exception:
    # fallback style
    style.configure("TButton", font=("Segoe UI", 12), padding=10)
    style.configure("TLabel", font=("Segoe UI", 12), background="#f8fafb")
    style.configure("TScale", background="#f8fafb")

frame = ttk.Frame(fenetre, padding=25, style="Card.TFrame")
frame.place(relx=0.5, rely=0.5, anchor="center")

# -- Affichage principal du timer --
timer_var = tk.StringVar()
timer_var.set("Arrêté")
timer_label = ttk.Label(frame, textvariable=timer_var, font=("Segoe UI", 38, "bold"), anchor="center")
timer_label.pack(pady=(0, 20))

# -- Entrées pour délai et durée bip --
def entry_style(entry):
    entry.configure(font=("Segoe UI", 12), justify="center")
    entry.pack(fill="x", pady=3)

ttk.Label(frame, text="Décompte (s)", font=("Segoe UI", 10)).pack(anchor="w")
entry_attente = ttk.Entry(frame)
entry_attente.insert(0, str(DELAI_PAR_DEFAUT))
entry_style(entry_attente)

ttk.Label(frame, text="Durée bip (s)", font=("Segoe UI", 10)).pack(anchor="w")
entry_duree = ttk.Entry(frame)
entry_duree.insert(0, str(DUREE_BIP_PAR_DEFAUT))
entry_style(entry_duree)

# -- Slider volume --
def maj_volume(val):
    volume_show.set(f"{int(float(val))}%")

ttk.Label(frame, text="Volume", font=("Segoe UI", 10)).pack(anchor="w")
volume_show = tk.StringVar(value=f"{VOLUME_PAR_DEFAUT}%")
scale_volume = ttk.Scale(frame, from_=0, to=100, orient=tk.HORIZONTAL, command=maj_volume, length=180)
scale_volume.set(VOLUME_PAR_DEFAUT)
scale_volume.pack(fill="x", pady=(0, 2))
ttk.Label(frame, textvariable=volume_show, font=("Segoe UI", 9, "italic"), foreground="#8a8a8a").pack(anchor="e", pady=(0, 10))

# -- Boutons --
btns = ttk.Frame(frame)
btns.pack(pady=(10,0))

alarme = Alarme()
ttk.Button(btns, text="Démarrer", command=alarme.demarrer, style="Accent.TButton").pack(side="left", padx=5)
ttk.Button(btns, text="Arrêter", command=alarme.arreter).pack(side="left", padx=5)

fenetre.mainloop()