import time
import threading
import tkinter as tk
from tkinter import ttk
import os

# Essayez d'importer pygame pour un vrai contrôle du volume
try:
    import pygame
    HAS_PYGAME = True
except ImportError:
    HAS_PYGAME = False

DELAI_PAR_DEFAUT = 210
DUREE_BIP_PAR_DEFAUT = 5
VOLUME_PAR_DEFAUT = 100
BIP_SOUND = "bip.wav"  # Placez un petit fichier bip.wav dans le dossier du script

class Alarme:
    def __init__(self):
        self.active = False
        self.thread = None
        self.attente = DELAI_PAR_DEFAUT
        self.duree_bip = DUREE_BIP_PAR_DEFAUT
        self.compteur = self.attente
        self.stop_event = threading.Event()
        if HAS_PYGAME:
            pygame.mixer.init()
            if os.path.exists(BIP_SOUND):
                self.sound = pygame.mixer.Sound(BIP_SOUND)
            else:
                self.sound = None

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
            return
        if HAS_PYGAME and self.sound:
            self.sound.set_volume(volume / 100)
            self.sound.play()
        else:
            # Fallback avec winsound (Windows uniquement, pas de contrôle du volume)
            import platform
            if platform.system() == "Windows":
                import winsound
                winsound.Beep(1000, 500)

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

# --- Interface graphique moderne ---
fenetre = tk.Tk()
fenetre.title("Minuteur Moderne")
fenetre.geometry("390x370")
fenetre.configure(bg="#20232a")

style = ttk.Style()
style.theme_use("clam")
style.configure("TFrame", background="#282c34")
style.configure("TLabel", background="#282c34", foreground="#ededed", font=("Segoe UI", 13))
style.configure("TButton", font=("Segoe UI", 13, "bold"), padding=10, borderwidth=0, relief="flat")
style.configure("Accent.TButton", background="#3fa8f4", foreground="#fff", borderwidth=0, relief="flat")
style.map("Accent.TButton",
    background=[("active", "#3291d7"), ("!active", "#3fa8f4")],
    foreground=[("active", "#fff")])
style.configure("Big.TLabel", background="#282c34", foreground="#fff", font=("Segoe UI", 38, "bold"))
style.configure("Volume.TLabel", background="#282c34", foreground="#7fc4f7", font=("Segoe UI", 18, "bold"))

frame = ttk.Frame(fenetre, padding=30, style="TFrame")
frame.place(relx=0.5, rely=0.5, anchor="center")

timer_var = tk.StringVar()
timer_var.set("Arrêté")
timer_label = ttk.Label(frame, textvariable=timer_var, style="Big.TLabel")
timer_label.pack(pady=(0, 28))

def entry_style(entry):
    entry.configure(font=("Segoe UI", 13), justify="center")
    entry.pack(fill="x", pady=6, ipady=3)

ttk.Label(frame, text="Décompte (s)").pack(anchor="w")
entry_attente = ttk.Entry(frame)
entry_attente.insert(0, str(DELAI_PAR_DEFAUT))
entry_style(entry_attente)

ttk.Label(frame, text="Durée bip (s)").pack(anchor="w")
entry_duree = ttk.Entry(frame)
entry_duree.insert(0, str(DUREE_BIP_PAR_DEFAUT))
entry_style(entry_duree)

# Slider volume moderne et fin avec pourcentage centré
def maj_volume(val):
    volume_show.set(f"{int(float(val))}%")

ttk.Label(frame, text="Volume").pack(anchor="w", pady=(5,0))
slider_frame = ttk.Frame(frame, style="TFrame")
slider_frame.pack(fill="x")

scale_volume = tk.Scale(slider_frame, from_=0, to=100, orient=tk.HORIZONTAL, showvalue=0,
                        length=220, command=maj_volume, sliderlength=14, width=5,
                        bg="#282c34", highlightthickness=0, troughcolor="#3fa8f4",
                        bd=0, fg="#fff", activebackground="#7fc4f7")
scale_volume.set(VOLUME_PAR_DEFAUT)
scale_volume.pack(pady=(2, 0), padx=10)
volume_show = tk.StringVar(value=f"{VOLUME_PAR_DEFAUT}%")
volume_label = ttk.Label(frame, textvariable=volume_show, style="Volume.TLabel", anchor="center")
volume_label.pack(pady=(0, 12))

btns = ttk.Frame(frame, style="TFrame")
btns.pack(pady=(10,0))

alarme = Alarme()
ttk.Button(btns, text="Démarrer", command=alarme.demarrer, style="Accent.TButton").pack(side="left", padx=7)
ttk.Button(btns, text="Arrêter", command=alarme.arreter).pack(side="left", padx=7)

# Message discret si pygame n'est pas installé
if not HAS_PYGAME:
    txt = "Astuce : installe pygame et ajoute bip.wav pour régler le volume du bip."
    ttk.Label(frame, text=txt, font=("Segoe UI", 8), foreground="#6a7b8a", background="#282c34").pack(pady=(14,0))

fenetre.mainloop()