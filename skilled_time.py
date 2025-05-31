import time
import threading
import tkinter as tk
from tkinter import ttk
import winsound

# Configuration initiale par défaut
defaut_attente = 210  # 3 minutes 30 secondes
defaut_duree_bip = 5  # secondes
defaut_volume = 100  # pourcentage (simulation, non fonctionnel avec winsound)

class Alarme:
    def __init__(self):
        self.active = False
        self.thread = None
        self.attente = defaut_attente
        self.duree_bip = defaut_duree_bip
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
            timer_var.set("Bips en cours")
            fin = time.time() + self.duree_bip
            while time.time() < fin and not self.stop_event.is_set():
                self.jouer_bip()
                time.sleep(1)
            self.compteur = self.attente
        timer_var.set("Alarme arrêtée")

    def jouer_bip(self):
        volume = int(scale_volume.get())
        if volume == 0:
            return  # silence simulé
        # winsound.Beep ne gère pas le volume, donc le son est toujours maximum
        frequency = 1000  # Hz
        duration = 500    # ms
        winsound.Beep(frequency, duration)
        # Pour un vrai contrôle du volume, utiliser pygame.mixer ou autre

    def demarrer(self):
        try:
            self.attente = int(entry_attente.get())
            self.duree_bip = int(entry_duree.get())
            self.compteur = self.attente
        except ValueError:
            timer_var.set("Valeurs invalides !")
            return

        if not self.active:
            self.active = True
            self.stop_event.clear()
            self.thread = threading.Thread(target=self.boucle_alarme, daemon=True)
            self.thread.start()
            timer_var.set("Alarme en attente...")

    def arreter(self):
        if self.active:
            self.active = False
            self.stop_event.set()
            self.compteur = self.attente
            timer_var.set("Alarme arrêtée")

# Interface graphique
alarme = Alarme()
fenetre = tk.Tk()
fenetre.title("Alarme Boucle Simple")
fenetre.geometry("400x250")
fenetre.configure(bg="#f5f5f5")

style = ttk.Style()
style.configure("TButton", font=("Segoe UI", 10), padding=6)
style.configure("TLabel", background="#f5f5f5", font=("Segoe UI", 10))

frame = ttk.Frame(fenetre, padding=20)
frame.pack(expand=True)

tt_label1 = ttk.Label(frame, text="Délai avant bip (s) :")
tt_label1.pack(anchor="w")
entry_attente = ttk.Entry(frame)
entry_attente.insert(0, str(defaut_attente))
entry_attente.pack(fill="x", pady=5)

tt_label2 = ttk.Label(frame, text="Durée des bips (s) :")
tt_label2.pack(anchor="w")
entry_duree = ttk.Entry(frame)
entry_duree.insert(0, str(defaut_duree_bip))
entry_duree.pack(fill="x", pady=5)

volume_var = tk.StringVar()
volume_var.set(f"Volume: {defaut_volume}%")

def update_volume(val):
    volume_var.set(f"Volume: {int(float(val))}%")

ttk.Label(frame, text="Volume (%) :").pack(anchor="w")
scale_volume = ttk.Scale(frame, from_=0, to=100, orient=tk.HORIZONTAL, command=update_volume, length=300)
scale_volume.set(defaut_volume)
scale_volume.pack(fill="x")
ttk.Label(frame, textvariable=volume_var).pack(anchor="center", pady=5)

btn_start = ttk.Button(frame, text="Activer", command=alarme.demarrer)
btn_start.pack(fill="x", pady=5)

btn_stop = ttk.Button(frame, text="Désactiver", command=alarme.arreter)
btn_stop.pack(fill="x", pady=5)

timer_var = tk.StringVar()
timer_var.set("Alarme arrêtée")
timer_label = ttk.Label(frame, textvariable=timer_var, font=("Segoe UI", 12, "bold"))
timer_label.pack(pady=20)

# SUPPRIME : le second label de décompte

# Message d'avertissement sur le volume
warn_label = ttk.Label(frame, text="Note : Le volume n'est pas ajusté avec winsound.\nÀ 0% : silence, >0% : volume maximum.\nPour un vrai contrôle du volume, utilisez pygame.", foreground="red")
warn_label.pack(pady=5)

fenetre.mainloop()