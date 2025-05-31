import tkinter as tk
import threading
import time
import platform

# --- COULEURS ---
COLOR_BG = "#111114"             # fond noir moderne
COLOR_CARD = "#1E1E22"           # carte/timer noir-gris
COLOR_TEXT = "#FFFFFF"           # texte blanc
COLOR_BORDER = "#FF6B1A"         # orange pour les contours
COLOR_BTN = "#FF6B1A"            # orange bouton
COLOR_BTN_ACTIVE = "#FF944D"     # orange clair bouton hover
COLOR_SLIDER = "#FF6B1A"         # orange slider
COLOR_SLIDER_BG = "#333"         # fond barre slider
RADIUS = 18

def play_beep(style, volume):
    if volume == 0:
        return
    if platform.system() == "Windows":
        import winsound
        if style == "court":
            winsound.Beep(1200, 120)
        elif style == "long":
            winsound.Beep(800, 600)
        else:
            winsound.Beep(1000, 300)
    else:
        print("\a")

class Alarme:
    def __init__(self):
        self.active = False
        self.thread = None
        self.stop_event = threading.Event()
        self.reset_values()

    def reset_values(self):
        self.attente = 210
        self.duree_bip = 5
        self.compteur = self.attente

    def boucle_alarme(self):
        self.compteur = self.attente
        while not self.stop_event.is_set():
            update_timer(f"{self.compteur // 60:02}:{self.compteur % 60:02}")
            while self.compteur > 0 and not self.stop_event.is_set():
                time.sleep(1)
                self.compteur -= 1
                update_timer(f"{self.compteur // 60:02}:{self.compteur % 60:02}")
            if self.stop_event.is_set():
                break
            update_timer("⏰ Bip ⏰")
            fin = time.time() + self.duree_bip
            while time.time() < fin and not self.stop_event.is_set():
                beep_style = beep_style_var.get()
                volume = int(volume_var.get())
                play_beep(beep_style, volume)
                time.sleep(1)
            self.compteur = self.attente
        update_timer("Arrêté")

    def demarrer(self):
        try:
            self.attente = int(entry_attente.get())
            self.duree_bip = int(entry_duree.get())
            self.compteur = self.attente
        except ValueError:
            update_timer("Erreur")
            return
        if not self.active:
            self.active = True
            self.stop_event.clear()
            self.thread = threading.Thread(target=self.boucle_alarme, daemon=True)
            self.thread.start()
            update_timer(f"{self.compteur // 60:02}:{self.compteur % 60:02}")

    def arreter(self):
        if self.active:
            self.active = False
            self.stop_event.set()
            self.compteur = self.attente
            update_timer("Arrêté")

def rounded_entry(parent, var, font, width=10, height=2):
    frame = tk.Frame(parent, bg=COLOR_BG, highlightbackground=COLOR_BORDER,
                     highlightcolor=COLOR_BORDER, highlightthickness=2, bd=0)
    entry = tk.Entry(frame, textvariable=var, font=font, width=width, bd=0,
                     justify="center", bg=COLOR_CARD, fg=COLOR_TEXT, relief="flat",
                     insertbackground=COLOR_TEXT, highlightthickness=0)
    entry.pack(ipady=10, fill="x")
    frame.pack_propagate(0)
    return frame, entry

def rounded_button(parent, text, command, font, bg=COLOR_BTN, fg=COLOR_TEXT):
    def on_enter(e): btn["bg"] = COLOR_BTN_ACTIVE
    def on_leave(e): btn["bg"] = bg
    btn = tk.Button(parent, text=text, command=command, bg=bg, fg=fg,
                    activebackground=COLOR_BTN_ACTIVE, activeforeground=fg,
                    font=font, bd=0, relief="flat", highlightthickness=0,
                    padx=18, pady=10, cursor="hand2")
    btn.pack_propagate(0)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn

def draw_slider(parent, var, width=220, height=36):
    canvas = tk.Canvas(parent, width=width, height=height, bg=COLOR_BG, highlightthickness=0)
    slider_length = width - 40
    slider_height = 8
    slider_radius = 13

    def redraw(val):
        canvas.delete("all")
        # Track (background)
        y = height // 2
        canvas.create_line(20, y, 20 + slider_length, y, fill=COLOR_SLIDER_BG, width=slider_height, capstyle="round")
        # Track (filled)
        end = 20 + slider_length * (val / 100)
        canvas.create_line(20, y, end, y, fill=COLOR_SLIDER, width=slider_height, capstyle="round")
        # Thumb (arrondi)
        handle_x = end
        canvas.create_oval(handle_x - slider_radius, y - slider_radius,
                           handle_x + slider_radius, y + slider_radius,
                           fill=COLOR_SLIDER, outline=COLOR_SLIDER)
    def click(event):
        x = min(max(event.x, 20), 20 + slider_length)
        val = int(100 * (x - 20) / slider_length)
        var.set(val)
        redraw(val)
        showvol.set(f"{val}%")
    canvas.bind("<Button-1>", click)
    canvas.bind("<B1-Motion>", click)
    redraw(var.get())
    canvas.pack()
    return canvas, redraw

fenetre = tk.Tk()
fenetre.title("Minuteur Moderne")
fenetre.configure(bg=COLOR_BG)
fenetre.minsize(400, 570)

# Responsive font sizes
def get_sizes():
    h = fenetre.winfo_height()
    f_big = max(18, int(h/13))
    f_norm = max(12, int(h/34))
    f_btn = max(13, int(h/28))
    entry_w = 260
    entry_h = max(38, int(h/13))
    btn_w = max(120, int(h/4))
    btn_h = max(38, int(h/13))
    slider_w = 260
    slider_h = max(36, int(h/15))
    return f_big, f_norm, f_btn, entry_w, entry_h, btn_w, btn_h, slider_w, slider_h

# --- TIMER ---
timer_var = tk.StringVar(value="Arrêté")
def update_timer(val): timer_var.set(val)

timer_frame = tk.Frame(fenetre, bg=COLOR_BG)
timer_frame.pack(fill="x", pady=(25,10))
timer_label = tk.Label(timer_frame, textvariable=timer_var, bg=COLOR_CARD, fg=COLOR_TEXT,
                       font=("Segoe UI", 38, "bold"), justify="center", pady=18, padx=20, relief="flat")
timer_label.pack(pady=8, ipadx=8, ipady=5, anchor="center", fill="x")
timer_label.config(borderwidth=0, highlightbackground=COLOR_BORDER, highlightcolor=COLOR_BORDER, highlightthickness=2)

# --- CHAMPS DUREE/DECOMPTE ---
fields_frame = tk.Frame(fenetre, bg=COLOR_BG)
fields_frame.pack(pady=(4, 12), fill="x")

attente_var = tk.StringVar(value="210")
attente_label = tk.Label(fields_frame, text="Décompte (s)", bg=COLOR_BG, fg=COLOR_TEXT, font=("Segoe UI", 14, "bold"))
attente_label.pack(anchor="center")
attente_frame, entry_attente = rounded_entry(fields_frame, attente_var, ("Segoe UI", 18, "bold"))
attente_frame.pack(pady=5, padx=30, fill="x")

duree_var = tk.StringVar(value="5")
duree_label = tk.Label(fields_frame, text="Durée bip (s)", bg=COLOR_BG, fg=COLOR_TEXT, font=("Segoe UI", 14, "bold"))
duree_label.pack(anchor="center")
duree_frame, entry_duree = rounded_entry(fields_frame, duree_var, ("Segoe UI", 18, "bold"))
duree_frame.pack(pady=5, padx=30, fill="x")

# --- SLIDER ---
slider_frame = tk.Frame(fenetre, bg=COLOR_BG)
slider_frame.pack(pady=(12,4))
volume_label = tk.Label(slider_frame, text="Volume", bg=COLOR_BG, fg=COLOR_TEXT, font=("Segoe UI", 14, "bold"))
volume_label.pack(anchor="center")
volume_var = tk.DoubleVar(value=100)
showvol = tk.StringVar(value="100%")
slider_canvas, slider_redraw = draw_slider(slider_frame, volume_var, 260, 38)
tk.Label(slider_frame, textvariable=showvol, bg=COLOR_BG, fg=COLOR_TEXT, font=("Segoe UI", 15, "bold")).pack(anchor="center", pady=(0,6))

# --- BOUTONS SON DU BIP ---
beep_style_var = tk.StringVar(value="classique")
beep_frame = tk.Frame(fenetre, bg=COLOR_BG)
beep_frame.pack(pady=(0, 10))
tk.Label(beep_frame, text="Son du bip", bg=COLOR_BG, fg=COLOR_TEXT, font=("Segoe UI", 14, "bold")).pack(anchor="center")
bip_choix = tk.Frame(beep_frame, bg=COLOR_BG)
bip_choix.pack()
def style_btn(val, btn):
    def select():
        beep_style_var.set(val)
        for b in btns_bip:
            b.config(bg=COLOR_CARD, fg=COLOR_TEXT)
        btn.config(bg=COLOR_BTN, fg=COLOR_TEXT)
    return select
btns_bip = []
for name, label in [("classique", "Classique"), ("court", "Court"), ("long", "Long")]:
    btn = tk.Button(bip_choix, text=label, bg=COLOR_BTN if name=="classique" else COLOR_CARD,
                    fg=COLOR_TEXT, font=("Segoe UI", 13, "bold"),
                    bd=0, padx=18, pady=8, relief="flat", highlightthickness=0,
                    activebackground=COLOR_BTN_ACTIVE, activeforeground=COLOR_TEXT,
                    command=style_btn(name, None))
    btns_bip.append(btn)
    btn.pack(side="left", padx=7)
for i, btn in enumerate(btns_bip):
    btn.config(command=style_btn(["classique", "court", "long"][i], btn))

# --- BOUTONS PRINCIPAUX ---
btns = tk.Frame(fenetre, bg=COLOR_BG)
btns.pack(pady=20)
alarme = Alarme()
start_btn = rounded_button(
    btns, "Démarrer", alarme.demarrer, ("Segoe UI", 16, "bold"),
    bg=COLOR_BTN, fg=COLOR_TEXT
)
start_btn.pack(side="left", padx=14, ipadx=12, ipady=6)
stop_btn = rounded_button(
    btns, "Arrêter", alarme.arreter, ("Segoe UI", 16, "bold"),
    bg=COLOR_CARD, fg=COLOR_TEXT
)
stop_btn.pack(side="left", padx=14, ipadx=12, ipady=6)

# --- RESPONSIVE auto FONT & ELEMENTS ---
def on_resize(event=None):
    f_big, f_norm, f_btn, entry_w, entry_h, btn_w, btn_h, slider_w, slider_h = get_sizes()
    timer_label.config(font=("Segoe UI", f_big, "bold"), padx=20, pady=18)
    attente_label.config(font=("Segoe UI", f_norm, "bold"))
    duree_label.config(font=("Segoe UI", f_norm, "bold"))
    entry_attente.config(font=("Segoe UI", f_btn, "bold"))
    entry_duree.config(font=("Segoe UI", f_btn, "bold"))
    volume_label.config(font=("Segoe UI", f_norm, "bold"))
    for b in btns_bip:
        b.config(font=("Segoe UI", f_btn, "bold"), padx=18, pady=8)
    start_btn.config(font=("Segoe UI", f_btn+2, "bold"), padx=22, pady=10)
    stop_btn.config(font=("Segoe UI", f_btn+2, "bold"), padx=22, pady=10)
    slider_canvas.config(width=slider_w, height=slider_h)
    slider_redraw(volume_var.get())
fenetre.bind("<Configure>", on_resize)
fenetre.after(300, on_resize)

fenetre.mainloop()