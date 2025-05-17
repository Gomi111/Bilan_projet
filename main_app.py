import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import date
import os
import sys
import pdf_generator

def start_main_app():
    # Database connection
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Main window setup
    root = tk.Tk()
    root.title("BilanPLUS ")
    root.geometry("1100x750")
    root.configure(bg='#f0f0f0')

    # Function definitions must come BEFORE they're referenced in buttons
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
                # Ouvrir le PDF automatiquement
                if os.name == 'nt':  # Windows
                    os.startfile(pdf_path)
                elif os.name == 'posix':  # Mac/Linux
                    os.system(f'open "{pdf_path}"' if sys.platform == 'darwin' else f'xdg-open "{pdf_path}"')
                
                # Message après l'ouverture du PDF
                messagebox.showinfo("Succès", f"PDF généré avec les dernières données:\n{pdf_path}")
            else:
                messagebox.showwarning("Avertissement", "Aucune donnée disponible pour générer le PDF")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de générer le PDF: {str(e)}")

    # Main container (3 parts: header, middle, buttons)
    main_container = tk.Frame(root, bg='#f0f0f0')
    main_container.pack(fill=tk.BOTH, expand=True)

    # 1. HEADER FRAME (always visible)
    header_frame = tk.Frame(main_container, bg='#f0f0f0')
    header_frame.pack(fill=tk.X, pady=(0, 5))

    date_du_jour = date.today().strftime("%Y-%m-%d")
    tk.Label(header_frame, 
            text=f"BilanPLUS - {date_du_jour}",
            font=("Helvetica", 14, "bold"),
            bg='#f0f0f0').pack()

    # 2. MIDDLE FRAME (scrollable content)
    middle_frame = tk.Frame(main_container, bg='#f0f0f0')
    middle_frame.pack(fill=tk.BOTH, expand=True)

    # Canvas and scrollbar
    canvas = tk.Canvas(middle_frame, bg='white', highlightthickness=0)
    scrollbar = tk.Scrollbar(middle_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Content frame inside canvas
    content_frame = tk.Frame(canvas, bg='white')
    canvas.create_window((0, 0), window=content_frame, anchor="nw")
    
    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig('content_frame', width=event.width)
    
    content_frame.bind("<Configure>", on_frame_configure)

    # Form sections - 2 columns layout
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
    
    # Create two columns for sections
    left_column = tk.Frame(content_frame, bg='white')
    left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
    right_column = tk.Frame(content_frame, bg='white')
    right_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

    # Create form fields
    for i, (section_title, champs) in enumerate(sections.items()):
        parent = left_column if i % 2 == 0 else right_column
        section_frame = tk.LabelFrame(parent, text=section_title,
                                    font=("Helvetica", 10, "bold"),
                                    padx=5, pady=5, bg='white')
        section_frame.pack(fill=tk.X, padx=5, pady=5)
        
        for row, champ in enumerate(champs):
            tk.Label(section_frame, text=champ.replace("_", " ").capitalize() + ":",
                    anchor="w", width=20, bg='white').grid(row=row, column=0, sticky="w", padx=5, pady=2)
            entry = tk.Entry(section_frame, width=20)
            entry.grid(row=row, column=1, sticky="ew", padx=5, pady=2)
            entries[champ] = entry
        section_frame.grid_columnconfigure(1, weight=1)

    # 3. BUTTON FRAME (ALWAYS VISIBLE AT BOTTOM)
    button_frame = tk.Frame(main_container, bg='#f0f0f0')
    button_frame.pack(fill=tk.X, pady=(5, 5))

    # Valider button
    valider_btn = tk.Button(button_frame, text="VALIDER", command=valider,
                          bg="#4CAF50", fg="white", font=("Helvetica", 10, "bold"),
                          width=15, padx=10)
    valider_btn.pack(side=tk.LEFT, padx=10)

    # PDF Export button
    pdf_btn = tk.Button(button_frame, text="Exporter en PDF", command=exporter_pdf,
                      bg="#2196F3", fg="white", font=("Helvetica", 10),
                      width=15, padx=10)
    pdf_btn.pack(side=tk.LEFT, padx=10)

    root.mainloop()
    conn.close()

if __name__ == "__main__":
    start_main_app()