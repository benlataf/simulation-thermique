import tkinter as tk
from tkinter import ttk, StringVar, DoubleVar
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')  # Force le backend Tk

# === Paramètres géométriques du cylindre ===
diametre = 0.075   # m
hauteur = 0.15   # m
rayon = diametre / 2
volume = np.pi * rayon**2 * hauteur  # m³
surface = 2 * np.pi * rayon**2 + 2 * np.pi * rayon * hauteur  # m²

# === Températures ===
T_initial = 38         # °C
T_ambiante = 39        # °C

# === Matériaux et propriétés thermiques ===
materiaux = {
    "Aluminium": {"rho": 2700, "cp": 900},
    "Acier": {"rho": 7850, "cp": 490},
    "Cuivre": {"rho": 8960, "cp": 385},
    "Plastique (ABS)": {"rho": 1040, "cp": 1300},
}

# === Coefficients de convection (ventilation) ===
h_values = [10, 25, 50]  # W/m²·K
linestyles = ['-', '--', ':']  # Pour les h croissants

# === Couleurs par matériau ===
couleurs_materiaux = {
    "Aluminium": 'blue',
    "Acier": 'red',
    "Cuivre": 'green',
    "Plastique (ABS)": 'purple'
}

# === Temps de simulation ===
t = np.linspace(0, 10800, 500)  # en secondes (0 à 3 h)



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
        plt.axhline(T_env, color='gray', linestyle='--', label="Température ambiante")
        plt.xlabel("Temps (minutes)")
        plt.ylabel("Température (°C)")
        plt.title("Simulation thermique d’un cylindre")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
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

tk.Label(root, text="Température ambiante (°C) :").grid(row=3, column=0, padx=10, pady=2, sticky="e")
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
