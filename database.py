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

# Suppression de l'ancienne table si elle existe
cursor.execute("DROP TABLE IF EXISTS suivi_journalier")

# Création de la table suivi_journalier avec tous les champs nécessaires
cursor.execute("""
CREATE TABLE suivi_journalier (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    
    -- Réceptions & Retours
    ca_co3_recep REAL,
    p2o5_recep REAL,
    h3po4_recep REAL,
    fuel_recep REAL,
    big_bag_recep REAL,
    ffs_recep REAL,
    cp6_recep REAL,
    housse_recep REAL,
    retour_mcp REAL,
    retour_cp6 REAL,

    -- Sorties & Évacuations
    vl_sortie REAL,
    export_m21 REAL,
    export_22 REAL,
    port_21 REAL,
    port_22 REAL,
    pnc_sortie REAL,

    -- Consommations
    ca_co3_cons REAL,
    p2o5_cons REAL,
    fuel_cons REAL,
    big_bag_cons REAL,
    ffs_cons REAL,
    housse_cons REAL,
    recyclage_cons REAL,
    cp6_cons REAL,

    -- Production & Ensachage
    vrac_21 REAL,
    lot_21 TEXT,
    vrac_22 REAL,
    lot_22 TEXT,
    vrac_lc REAL,
    lot_lc TEXT,
    vrac_nc REAL,
    bb_1t REAL,
    bb_1_1t REAL,
    sb_1t REAL,
    sb_1_25t REAL,
    prod_ffs REAL,
    prod_big_bag REAL,

    -- Relevé des stocks
    silo_a_caco3 REAL,
    silo_b_caco3 REAL,
    bac_h3po4_c1 REAL,
    silo_a_m21 REAL,
    silo_b_m21 REAL,
    silo_a_m22 REAL,
    silo_b_m22 REAL,
    bb1t_m21 REAL,
    bb1_1t_m21 REAL,
    sb1t_m21 REAL,
    sb1_25t_m21 REAL,
    bb1t_m22 REAL,
    bb1_1t_m22 REAL,
    sb1t_m22 REAL,
    sb1_25t_m22 REAL,
    pnc_stock REAL,
    stock_debut REAL,
    stock_fin REAL,

    -- Journal des arrêts
    arret_externe TEXT,
    arret_endogene TEXT,
    arret_programme TEXT,
    arret_process TEXT,
    arret_mmfd TEXT,
    arret_mefd TEXT,
    arret_mifd TEXT,
    arret_bm_gc TEXT,
    arret_gc TEXT,

    -- Rendements
    conso_specifique REAL,
    rendement REAL,

    -- Emballage
    bobine_utilisee REAL,
    housse_utilisee REAL
)
""")

conn.commit()
conn.close()

print("Base de données et tables créées avec succès.")