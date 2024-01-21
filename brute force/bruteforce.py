import time
import pyautogui

# Les quatre derniers chiffres de votre code
derniers_chiffres = '2515'

# Liste pour stocker les codes testés
codes_testes = []

# Compteur pour le nombre de combinaisons testées
compteur = 0
time.sleep(5)
# Générer toutes les combinaisons possibles pour les deux premiers chiffres
for i in range(10):
    for j in range(10):
        # Créer le code complet
        code_complet = str(i) + str(j) + derniers_chiffres
        # Ajouter le code à la liste des codes testés
        codes_testes.append(code_complet)
        # Si plus de 15 codes ont été testés, supprimer le plus ancien
        if len(codes_testes) > 15:
            codes_testes.pop(0)
        # "Taper" le code comme un humain
        pyautogui.write(code_complet)
        # Appuyer sur Entrée
        pyautogui.press('enter')
        # Incrémenter le compteur
        compteur += 1
        # Si 10 combinaisons ont été testées, attendre 5 secondes
        if compteur % 10 == 0:
            time.sleep(7)

# Écrire les codes testés dans un fichier
with open('codes_testes.txt', 'w') as f:
    for code in codes_testes:
        f.write(code + '\n')