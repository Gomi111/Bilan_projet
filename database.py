import sqlite3

# Connexion à la base (ou création si elle n'existe pas)
conn = sqlite3.connect("data.db")
cursor = conn.cursor()

# Création de la table admin (un seul admin ici)
cursor.execute("""
CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
""")

# Insertion d'un admin si aucun n'existe (ex: admin/admin)
cursor.execute("SELECT COUNT(*) FROM admin")
if cursor.fetchone()[0] == 0:
    cursor.execute("INSERT INTO admin (username, password) VALUES (?, ?)", ("admin", "admin"))

# Création d'une table exemple pour les saisies (on mettra plus tard les 30+ champs)
cursor.execute("""
CREATE TABLE IF NOT EXISTS suivi_journalier (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_jour TEXT NOT NULL,
    production_x REAL,
    production_y REAL,
    production_c REAL,
    consommation_matiere1 REAL,
    consommation_matiere2 REAL
    -- ajoute les autres champs plus tard
)
""")

conn.commit()
conn.close()

print("Base de données et tables créées avec succès.")
