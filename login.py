import tkinter as tk
from tkinter import messagebox
import sqlite3
import main_app

def verify_login():
    username = entry_username.get()
    password = entry_password.get()

    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admin WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()
    conn.close()

    if result:
        root.destroy()
        main_app.start_main_app()
    else:
        messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect")

# Fenêtre de login
root = tk.Tk()
root.title("BilanPLUS")
root.geometry("360x250")
root.configure(bg="#0D1B2A")

# Titre
label_title = tk.Label(root, text="BilanPLUS", font=("Helvetica", 18, "bold"),
                       fg="white", bg="#0D1B2A")
label_title.pack(pady=15)

# Zone de saisie Nom d'utilisateur
label_username = tk.Label(root, text="Nom d'utilisateur", font=("Helvetica", 10),
                          fg="white", bg="#0D1B2A")
label_username.pack()
entry_username = tk.Entry(root, font=("Helvetica", 10), bg="white", relief="flat", width=25)
entry_username.pack(pady=5)

# Zone de saisie Mot de passe
label_password = tk.Label(root, text="Mot de passe", font=("Helvetica", 10),
                          fg="white", bg="#0D1B2A")
label_password.pack()
entry_password = tk.Entry(root, show="*", font=("Helvetica", 10), bg="white", relief="flat", width=25)
entry_password.pack(pady=5)

# Bouton Se connecter
btn_login = tk.Button(root, text="Se connecter", command=verify_login,
                      bg="#1B998B", fg="white", font=("Helvetica", 10, "bold"),
                      activebackground="#14746F", relief="flat", width=20)
btn_login.pack(pady=20)

root.mainloop()
