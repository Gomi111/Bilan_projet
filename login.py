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
        main_app.open_main_app()  # Appeler l'interface principale
    else:
        messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect")

# Fenêtre de login
root = tk.Tk()
root.title("Connexion - BilanPLUS")
root.geometry("300x200")

label_title = tk.Label(root, text="BilanPLUS", font=("Arial", 16))
label_title.pack(pady=10)

tk.Label(root, text="Nom d'utilisateur").pack()
entry_username = tk.Entry(root)
entry_username.pack()

tk.Label(root, text="Mot de passe").pack()
entry_password = tk.Entry(root, show="*")
entry_password.pack()

btn_login = tk.Button(root, text="Se connecter", command=verify_login)
btn_login.pack(pady=10)

root.mainloop()
