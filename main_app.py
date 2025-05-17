import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import date
import os
import sys
import pdf_generator

def start_main_app():
    # Connexion DB
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Fenêtre principale
    root = tk.Tk()
    root.title("BilanPLUS")
    root.geometry("1100x750")
    root.configure(bg='#1E1E2F')  # fond plus foncé et moderne

    # ---- Fonctions ----
    def valider():
        valeurs = [date_du_jour]
        tous_les_champs = []
        for section in sections.values():
            for champ in section:
                tous_les_champs.append(champ)
                valeurs.append(entries[champ].get())
        try:
            cursor.execute(f"INSERT INTO suivi_journalier (date, {', '.join(tous_les_champs)}) VALUES ({','.join(['?']*len(valeurs))})", valeurs)
            conn.commit()
            messagebox.showinfo("Succès", "Données enregistrées")
            for champ in tous_les_champs:
                entries[champ].delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def exporter_pdf():
        try:
            pdf_path = pdf_generator.generate_pdf_from_db()
            if pdf_path:
                if os.name == 'nt':
                    os.startfile(pdf_path)
                elif os.name == 'posix':
                    os.system(f'open "{pdf_path}"' if sys.platform == 'darwin' else f'xdg-open "{pdf_path}"')
                messagebox.showinfo("Succès", f"PDF généré avec les dernières données:\n{pdf_path}")
            else:
                messagebox.showwarning("Avertissement", "Aucune donnée disponible pour générer le PDF")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de générer le PDF: {str(e)}")

    # ---- Structure principale ----
    main_container = tk.Frame(root, bg='#1E1E2F')
    main_container.pack(fill=tk.BOTH, expand=True)

    # ---- En-tête ----
    header_frame = tk.Frame(main_container, bg='#1E1E2F')
    header_frame.pack(fill=tk.X, pady=(0, 5))

    date_du_jour = date.today().strftime("%Y-%m-%d")
    tk.Label(header_frame, 
             text=f"BilanPLUS - {date_du_jour}",
             font=("Helvetica", 18, "bold"),
             bg='#1E1E2F',
             fg='white').pack()

    # ---- Contenu scrollable ----
    middle_frame = tk.Frame(main_container, bg='#1E1E2F')
    middle_frame.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(middle_frame, bg='#2D2F3A', highlightthickness=0)
    scrollbar = tk.Scrollbar(middle_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    canvas.configure(yscrollcommand=scrollbar.set)

    content_frame = tk.Frame(canvas, bg='#2D2F3A')
    canvas.create_window((0, 0), window=content_frame, anchor="nw")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig('content_frame', width=event.width)
    content_frame.bind("<Configure>", on_frame_configure)

    # ---- Champs ----
    sections = {
        "Réceptions": ["ca_co3_recep", "p2o5_recep", "h3po4_recep", "fuel_recep",
                      "big_bag_recep", "ffs_recep", "cp6_recep", "housse_recep"],
        "Consommations": ["ca_co3_cons", "p2o5_cons", "fuel_cons"],
        "Production": ["prod_ffs", "prod_big_bag"],
        "Stocks": ["stock_debut", "stock_fin"],
        "Arrêts": ["arret_externe", "arret_endogene", "arret_programme"],
        "Rendements": ["conso_specifique", "rendement"],
        "Emballage": ["bobine_utilisee", "housse_utilisee"]
    }

    entries = {}

    left_column = tk.Frame(content_frame, bg='#2D2F3A')
    left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
    right_column = tk.Frame(content_frame, bg='#2D2F3A')
    right_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

    for i, (section_title, champs) in enumerate(sections.items()):
        parent = left_column if i % 2 == 0 else right_column
        section_frame = tk.LabelFrame(parent, text=section_title,
                                      font=("Helvetica", 10, "bold"),
                                      padx=5, pady=5, 
                                      bg='#3A3D4D', fg='white',
                                      labelanchor='n')
        section_frame.pack(fill=tk.X, padx=5, pady=5)
        
        for row, champ in enumerate(champs):
            tk.Label(section_frame, 
                     text=champ.replace("_", " ").capitalize() + " :",
                     anchor="w", width=20, 
                     bg='#3A3D4D', fg='white').grid(row=row, column=0, sticky="w", padx=5, pady=2)
            entry = tk.Entry(section_frame, width=20, bg='#F5F5F5', fg='black')
            entry.grid(row=row, column=1, sticky="ew", padx=5, pady=2)
            entries[champ] = entry
        section_frame.grid_columnconfigure(1, weight=1)

    # ---- Boutons ----
    button_frame = tk.Frame(main_container, bg='#1E1E2F')
    button_frame.pack(fill=tk.X, pady=(5, 5))

    valider_btn = tk.Button(button_frame, text="VALIDER", command=valider,
                            bg="#283d99", fg="white", font=("Helvetica", 11, "bold"),
                            width=18, padx=10, pady=5, relief=tk.FLAT)
    valider_btn.pack(side=tk.LEFT, padx=15)

    pdf_btn = tk.Button(button_frame, text="Exporter en PDF", command=exporter_pdf,
                        bg="#1B998B", fg="white", font=("Helvetica", 11),
                        width=18, padx=10, pady=5, relief=tk.FLAT)
    pdf_btn.pack(side=tk.LEFT, padx=10)

    root.mainloop()
    conn.close()

if __name__ == "__main__":
    start_main_app()
