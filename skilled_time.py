import time, threading, platform
import customtkinter as ctk
from tkinter import StringVar, IntVar

COLOR_BG = "#111114"
COLOR_CARD = "#1E1E22"
COLOR_TEXT = "#FFFFFF"
COLOR_BORDER = "#FF6B1A"
COLOR_BTN = "#FF6B1A"
COLOR_BTN_HOVER = "#FF944D"
COLOR_SLIDER_BG = "#333333"
COLOR_SLIDER = "#FF6B1A"

RADIUS_CARD = 18
RADIUS_ENTRY = 15
RADIUS_BTN = 15

DELAI_DEF, DUREE_DEF, VOLUME_DEF = 210, 5, 100


def play_beep(style: str, volume: int):
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
    def __init__(self, update_ui):
        self.update_ui = update_ui
        self.stop_evt = threading.Event()
        self.active = False
        self.reset()

    def reset(self):
        self.attente, self.duree_bip = DELAI_DEF, DUREE_DEF
        self.compteur = self.attente

    def _loop(self):
        self.compteur = self.attente
        while not self.stop_evt.is_set():
            while self.compteur > 0 and not self.stop_evt.is_set():
                m, s = divmod(self.compteur, 60)
                self.update_ui(f"{m:02}:{s:02}")
                time.sleep(1)
                self.compteur -= 1
            if self.stop_evt.is_set():
                break
            self.update_ui("⏰ Bip ⏰")
            t_end = time.time() + self.duree_bip
            while time.time() < t_end and not self.stop_evt.is_set():
                play_beep(app.beep_style_var.get(), app.volume_var.get())
                time.sleep(1)
            self.compteur = self.attente
        self.update_ui("Arrêté")

    def start(self, attente_s, duree_s):
        if self.active:
            return
        try:
            self.attente = int(attente_s)
            self.duree_bip = int(duree_s)
            self.compteur = self.attente
        except ValueError:
            self.update_ui("Erreur")
            return
        self.active = True
        self.stop_evt.clear()
        threading.Thread(target=self._loop, daemon=True).start()
        m, s = divmod(self.compteur, 60)
        self.update_ui(f"{m:02}:{s:02}")

    def stop(self):
        if self.active:
            self.active = False
            self.stop_evt.set()


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        self.title("Minuteur Moderne")
        self.configure(fg_color=COLOR_BG)
        self.minsize(380, 550)

        self.timer_var = StringVar(value="Arrêté")
        self.volume_var = IntVar(value=VOLUME_DEF)
        self.beep_style_var = StringVar(value="classique")

        self.card = ctk.CTkFrame(
            self,
            width=340,
            height=500,
            fg_color=COLOR_CARD,
            corner_radius=RADIUS_CARD,
            border_width=2,
            border_color=COLOR_BORDER,
        )
        self.card.place(relx=0.5, rely=0.5, anchor="center")

        lbl_frame = ctk.CTkFrame(
            self.card,
            fg_color="transparent",
            corner_radius=RADIUS_CARD - 4,
            border_width=2,
            border_color=COLOR_BORDER,
        )
        lbl_frame.pack(pady=(20, 20), padx=20, fill="x")
        self.lbl_timer = ctk.CTkLabel(
            lbl_frame,
            textvariable=self.timer_var,
            text_color=COLOR_TEXT,
            fg_color="transparent",
            font=("Segoe UI", 38, "bold"),
        )
        self.lbl_timer.pack(ipady=4)

        fields = ctk.CTkFrame(self.card, fg_color="transparent")
        fields.pack(pady=(0, 10), fill="x")

        self._add_label(fields, "Décompte (s)")
        self.attente_var = StringVar(value=str(DELAI_DEF))
        self.entry_attente = self._add_entry(fields, self.attente_var)

        self._add_label(fields, "Durée bip (s)")
        self.duree_var = StringVar(value=str(DUREE_DEF))
        self.entry_duree = self._add_entry(fields, self.duree_var)

        self._add_label(self.card, "Volume")
        self.slider = ctk.CTkSlider(
            self.card,
            from_=0,
            to=100,
            variable=self.volume_var,
            command=self._show_vol,
            fg_color=COLOR_SLIDER_BG,
            progress_color=COLOR_SLIDER,
            button_color=COLOR_SLIDER,
            button_hover_color=COLOR_BTN_HOVER,
        )
        self.slider.pack(pady=(0, 4), padx=20, fill="x")
        self.vol_label = ctk.CTkLabel(
            self.card,
            text=f"{VOLUME_DEF}%",
            text_color=COLOR_TEXT,
            font=("Segoe UI", 16, "bold"),
        )
        self.vol_label.pack(pady=(0, 12))

        self._add_label(self.card, "Son du bip")
        beep_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        beep_frame.pack(pady=(0, 12))
        self.btn_bip_classique = self._add_beep_btn(
            beep_frame, "Classique", "classique"
        )
        self.btn_bip_court = self._add_beep_btn(beep_frame, "Court", "court")
        self.btn_bip_long = self._add_beep_btn(beep_frame, "Long", "long")
        self._select_beep("classique")

        btns = ctk.CTkFrame(self.card, fg_color="transparent")
        btns.pack(pady=(10, 0))
        self.start_btn = ctk.CTkButton(
            btns,
            text="Démarrer",
            fg_color=COLOR_BTN,
            hover_color=COLOR_BTN_HOVER,
            text_color=COLOR_TEXT,
            corner_radius=RADIUS_BTN,
            font=("Segoe UI", 16, "bold"),
            command=self._on_start,
        )
        self.start_btn.pack(side="left", padx=10, ipadx=10, ipady=6)
        self.stop_btn = ctk.CTkButton(
            btns,
            text="Arrêter",
            fg_color=COLOR_CARD,
            hover_color=COLOR_SLIDER_BG,
            text_color=COLOR_TEXT,
            corner_radius=RADIUS_BTN,
            font=("Segoe UI", 16, "bold"),
            command=self._on_stop,
        )
        self.stop_btn.pack(side="left", padx=10, ipadx=10, ipady=6)

        self.alarme = Alarme(self._safe_timer_update)
        self.bind("<Configure>", self._on_resize)
        self.after(200, self._on_resize)

    def _add_label(self, parent, txt):
        ctk.CTkLabel(
            parent,
            text=txt,
            text_color=COLOR_TEXT,
            font=("Segoe UI", 14, "bold"),
            fg_color="transparent",
        ).pack(anchor="center", pady=(6, 0))

    def _add_entry(self, parent, tkvar):
        wrap = ctk.CTkFrame(
            parent,
            fg_color=COLOR_CARD,
            corner_radius=RADIUS_ENTRY,
            border_width=2,
            border_color=COLOR_BORDER,
        )
        ent = ctk.CTkEntry(
            wrap,
            textvariable=tkvar,
            justify="center",
            fg_color=COLOR_CARD,
            text_color=COLOR_TEXT,
            font=("Segoe UI", 18, "bold"),
            corner_radius=RADIUS_ENTRY - 2,
            border_width=0,
        )
        ent.pack(fill="x", ipady=8)
        wrap.pack(pady=(4, 8), padx=20, fill="x")
        return ent

    def _add_beep_btn(self, parent, txt, value):
        btn = ctk.CTkButton(
            parent,
            text=txt,
            width=100,
            height=40,
            fg_color=COLOR_CARD,
            hover_color=COLOR_SLIDER_BG,
            text_color=COLOR_TEXT,
            corner_radius=RADIUS_BTN,
            font=("Segoe UI", 13, "bold"),
            command=lambda v=value: self._select_beep(v),
        )
        btn.pack(side="left", padx=6)
        return btn

    def _select_beep(self, value):
        self.beep_style_var.set(value)
        for b in (self.btn_bip_classique, self.btn_bip_court, self.btn_bip_long):
            b.configure(fg_color=COLOR_CARD)
        if value == "classique":
            self.btn_bip_classique.configure(fg_color=COLOR_BTN)
        elif value == "court":
            self.btn_bip_court.configure(fg_color=COLOR_BTN)
        else:
            self.btn_bip_long.configure(fg_color=COLOR_BTN)

    def _show_vol(self, v):
        self.vol_label.configure(text=f"{int(float(v))}%")

    def _safe_timer_update(self, txt):
        self.after(0, lambda: self.timer_var.set(txt))

    def _on_start(self):
        self.alarme.start(self.entry_attente.get(), self.entry_duree.get())

    def _on_stop(self):
        self.alarme.stop()

    def _on_resize(self, _=None):
        h = self.winfo_height()
        big = max(24, int(h / 15))
        norm = max(12, int(h / 40))
        btnf = max(14, int(h / 34))
        self.lbl_timer.configure(font=("Segoe UI", big, "bold"))
        self.entry_attente.configure(font=("Segoe UI", btnf, "bold"))
        self.entry_duree.configure(font=("Segoe UI", btnf, "bold"))
        self.slider.configure(height=max(20, int(h / 48)))
        for b in (self.btn_bip_classique, self.btn_bip_court, self.btn_bip_long):
            b.configure(font=("Segoe UI", btnf, "bold"))
        self.start_btn.configure(font=("Segoe UI", btnf + 2, "bold"))
        self.stop_btn.configure(font=("Segoe UI", btnf + 2, "bold"))


if __name__ == "__main__":
    app = App()
    app.mainloop()