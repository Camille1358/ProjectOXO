import time
import pyautogui

# Les quatre derniers chiffres de votre code
derniers_chiffres = '2515'
time.sleep(3)
# Générer toutes les combinaisons possibles pour les deux premiers chiffres
for i in range(10):
    for j in range(10):
        # Créer le code complet
        code_complet = str(i) + str(j) + derniers_chiffres
        # Attendre 2 secondes
        time.sleep(1)
        # "Taper" le code comme un humain
        pyautogui.write(code_complet)
        # Appuyer sur Entrée
        pyautogui.press('enter')