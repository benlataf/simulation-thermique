__version__ = "dev"
import tkinter as tk
from tkinter import ttk, StringVar, DoubleVar
import numpy as np
import matplotlib.pyplot as plt
plt.ion()  # Activate interactive mode so show() doesn't block Tkinter
import matplotlib
matplotlib.use('TkAgg')  # Force le backend Tk

# === Matériaux et propriétés thermiques ===
materiaux = {
    "Aluminium": {"rho": 2700, "cp": 900},
    "Acier": {"rho": 7850, "cp": 490},
    "Cuivre": {"rho": 8960, "cp": 385},
    "Plastique (ABS)": {"rho": 1040, "cp": 1300},
}

couleurs_materiaux = {
    "Aluminium": "blue",
    "Acier": "red",
    "Cuivre": "green",
    "Plastique (ABS)": "purple"
}

# === Temps de simulation ===
t = np.linspace(0, 18000, 500)  # en secondes (0 à 5 h)



# === Interface graphique Tkinter ===
def lancer_simulation():
    try:
        d_mm = float(entry_diametre.get())
        h_mm = float(entry_hauteur.get())
        T_init = float(entry_temp_init.get())
        T_env = float(entry_temp_amb.get())
        mat = combo_materiau.get()
        h_conv = float(combo_h.get())

        # Conversion mm → m
        diametre = d_mm / 1000
        hauteur = h_mm / 1000
        rayon = diametre / 2
        volume = np.pi * rayon**2 * hauteur
        surface = 2 * np.pi * rayon**2 + 2 * np.pi * rayon * hauteur

        rho, cp = materiaux[mat]["rho"], materiaux[mat]["cp"]
        couleur = couleurs_materiaux[mat]

        tau = (rho * cp * volume) / (h_conv * surface)
        T = T_env + (T_init - T_env) * np.exp(-t / tau)

        plt.figure(figsize=(8, 4))
        plt.plot(t / 60, T, label=f"{mat}, h={h_conv} W/m²K", color=couleur)
        # Calcul des temps caractéristiques
        t95 = -tau * np.log(0.05)
        t99 = -tau * np.log(0.01)
        t999 = -tau * np.log(0.001)
        # Tracer les lignes verticales
        plt.axvline(t95 / 60, color='orange', linestyle='--', label=f'95% atteint ({t95/60:.1f} min)')
        plt.axvline(t99 / 60, color='red', linestyle='--', label=f'99% atteint ({t99/60:.1f} min)')
        plt.axvline(t999 / 60, color='purple', linestyle=':', label=f'≈100% atteint ({t999/60:.1f} min)')
        plt.axhline(T_env, color='gray', linestyle='--', label="Température de l’enceinte")
        plt.xlabel("Temps (minutes)")
        plt.ylabel("Température (°C)")
        plt.title("Simulation thermique pour un cylindre (lumped capacity model)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show(block=False)
    except ValueError:
        print("Erreur : vérifiez que tous les champs sont bien remplis.")

root = tk.Tk()
root.title("Simulation Thermique Cylindre")

tk.Label(root, text="Diamètre (mm) :").grid(row=0, column=0, padx=10, pady=2, sticky="e")
entry_diametre = tk.Entry(root)
entry_diametre.insert(0, "75")
entry_diametre.grid(row=0, column=1)

tk.Label(root, text="Hauteur (mm) :").grid(row=1, column=0, padx=10, pady=2, sticky="e")
entry_hauteur = tk.Entry(root)
entry_hauteur.insert(0, "150")
entry_hauteur.grid(row=1, column=1)

tk.Label(root, text="Température initiale (°C) :").grid(row=2, column=0, padx=10, pady=2, sticky="e")
entry_temp_init = tk.Entry(root)
entry_temp_init.insert(0, "20")
entry_temp_init.grid(row=2, column=1)

tk.Label(root, text="Température de l’enceinte (°C) :").grid(row=3, column=0, padx=10, pady=2, sticky="e")
entry_temp_amb = tk.Entry(root)
entry_temp_amb.insert(0, "34")
entry_temp_amb.grid(row=3, column=1)

tk.Label(root, text="Matériau :").grid(row=4, column=0, padx=10, pady=2, sticky="e")
combo_materiau = ttk.Combobox(root, values=list(materiaux.keys()))
combo_materiau.current(0)
combo_materiau.grid(row=4, column=1)

tk.Label(root, text="h (W/m²·K) :").grid(row=5, column=0, padx=10, pady=2, sticky="e")
combo_h = ttk.Combobox(root, values=[10, 25, 50])
combo_h.current(0)
combo_h.grid(row=5, column=1)

bouton = tk.Button(root, text="Lancer simulation", command=lancer_simulation)
bouton.grid(row=6, column=0, columnspan=2, pady=10)

root.mainloop()
