import tkinter as tk

def open_main_app():
    main_root = tk.Tk()
    main_root.title("BilanPLUS")
    main_root.geometry("600x400")

    label = tk.Label(main_root, text="Bienvenue dans BilanPLUS", font=("Arial", 16))
    label.pack(pady=50)

    main_root.mainloop()
