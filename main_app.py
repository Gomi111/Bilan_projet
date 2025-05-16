import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import date
import os
import pdf_generator

def start_main_app():
    # Database connection
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Main window
    root = tk.Tk()
    root.title("BilanPLUS - Suivi Journalier")
    root.geometry("1100x700")

    # Scrollable canvas setup
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(main_frame)
    scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
    
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Content frame
    frame_content = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame_content, anchor="nw")
    frame_content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Current date header
    date_du_jour = date.today().strftime("%Y-%m-%d")
    tk.Label(frame_content, text=f"Bilan du {date_du_jour}", 
            font=("Helvetica", 16, "bold")).pack(pady=15)

    # Form sections
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

    # Create form fields
    for section_title, champs in sections.items():
        section_frame = tk.LabelFrame(frame_content, 
                                    text=section_title,
                                    font=("Helvetica", 12, "bold"),
                                    padx=10,
                                    pady=10)
        section_frame.pack(fill="x", padx=20, pady=10, expand=True)
        
        for i, champ in enumerate(champs):
            label = tk.Label(section_frame, 
                           text=champ.replace("_", " ").capitalize() + ":",
                           anchor="w",
                           width=25)
            label.grid(row=i, column=0, sticky="w", padx=5, pady=2)
            
            entry = tk.Entry(section_frame, width=30)
            entry.grid(row=i, column=1, sticky="ew", padx=5, pady=2)
            entries[champ] = entry
        
        section_frame.columnconfigure(1, weight=1)

    # Save data function
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

    # PDF export function
    def exporter_pdf():
        if pdf_generator.generate_pdf_from_db():
            today = date.today().strftime("%Y-%m-%d")
            pdf_file = f"bilan_{today}.pdf"
            try:
                os.startfile(pdf_file)
                messagebox.showinfo("Succès", f"PDF généré et ouvert: {pdf_file}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d'ouvrir le PDF: {str(e)}")
        else:
            messagebox.showwarning("Avertissement", "Aucune donnée disponible pour aujourd'hui")

    # Buttons
    tk.Button(frame_content, 
             text="VALIDER", 
             command=valider, 
             bg="green", 
             fg="white", 
             font=("Helvetica", 12, "bold")).pack(pady=20)

    tk.Button(frame_content, 
             text="Exporter en PDF", 
             command=exporter_pdf, 
             bg="lightblue", 
             font=("Helvetica", 12)).pack(pady=10)

    root.mainloop()
    conn.close()

if __name__ == "__main__":
    start_main_app()