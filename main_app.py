import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import date

# Connexion à la base de données
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Fenêtre principale
root = tk.Tk()
root.title("BilanPLUS - Suivi Journalier")
root.geometry("1100x700")

# Canvas pour scroll
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=1)

canvas = tk.Canvas(main_frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

frame_content = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame_content, anchor="nw")

# Date du jour en haut
date_du_jour = date.today().strftime("%Y-%m-%d")
tk.Label(frame_content, text=f"Bilan du {date_du_jour}", font=("Helvetica", 16, "bold")).pack(pady=15)

# Définir tous les champs (à adapter selon ta base réelle)
sections = {
    "Réceptions": [
        "ca_co3_recep", "p2o5_recep", "h3po4_recep", "fuel_recep",
        "big_bag_recep", "ffs_recep", "cp6_recep", "housse_recep"
    ],
    "Consommations": [
        "ca_co3_cons", "p2o5_cons", "fuel_cons"
    ],
    "Production": [
         "prod_ffs", "prod_big_bag"
    ],
    "Stocks": [
        "stock_debut", "stock_fin"
    ],
    "Arrêts": [
        "arret_externe", "arret_endogene", "arret_programme"
    ],
    "Rendements": [
        "conso_specifique", "rendement"
    ],
    "Emballage": [
        "bobine_utilisee", "housse_utilisee"
    ]
}

entries = {}

# Affichage des sections
for section_title, champs in sections.items():
    section_frame = tk.LabelFrame(frame_content, text=section_title, font=("Helvetica", 12, "bold"), padx=10, pady=10)
    section_frame.pack(fill="x", padx=20, pady=10)
    
    for i, champ in enumerate(champs):
        label = tk.Label(section_frame, text=champ.replace("_", " ").capitalize(), anchor="w", width=30)
        label.grid(row=i, column=0, sticky="w", pady=5)
        entry = tk.Entry(section_frame, width=40)
        entry.grid(row=i, column=1, pady=5)
        entries[champ] = entry

# Fonction de validation
def valider():
    valeurs = [date_du_jour]
    tous_les_champs = []

    for section in sections.values():
        for champ in section:
            tous_les_champs.append(champ)
            valeurs.append(entries[champ].get())

    try:
        cursor.execute(f'''
            INSERT INTO suivi_journalier (
                date, {', '.join(tous_les_champs)}
            ) VALUES ({','.join(['?'] * len(valeurs))})
        ''', valeurs)
        conn.commit()
        messagebox.showinfo("Succès", "Les données ont été enregistrées.")
        for champ in tous_les_champs:
            entries[champ].delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

#fonction d'exporter en PDF
from pdf_generator import generate_pdf_from_db

def exporter_pdf():
    success = generate_pdf_from_db()
    if success:
        messagebox.showinfo("PDF", "Le PDF du jour a été généré avec succès.")
    else:
        messagebox.showwarning("Aucune donnée", "Aucune donnée saisie aujourd’hui.")

# Bouton Valider
tk.Button(frame_content, text="VALIDER", command=valider, bg="green", fg="white", font=("Helvetica", 12, "bold")).pack(pady=30)

# Lancer la fenêtre
root.mainloop()
