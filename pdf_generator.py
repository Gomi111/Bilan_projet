# pdf_generator.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
import sqlite3
from datetime import datetime
import os
from pathlib import Path
# Configuration constants
REPORTS_DIR = Path.home() / "Documents" / "BilanPLUS_Reports"
#REPORTS_DIR = "generated_reports"  # Directory where all PDFs will be stored
MAX_REPORTS = 70  # Keep only last 30 reports

def generate_pdf_from_db(db_path='data.db'):
    try:
        # Create reports directory if it doesn't exist
        os.makedirs(REPORTS_DIR, exist_ok=True)
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Récupère le dernier enregistrement (le plus récent)
        cursor.execute("SELECT * FROM suivi_journalier ORDER BY date DESC, id DESC LIMIT 1")
        row = cursor.fetchone()

        if not row:
            return False

        # Récupère les noms des colonnes
        cursor.execute("PRAGMA table_info(suivi_journalier)")
        columns = [info[1] for info in cursor.fetchall()]
        data = dict(zip(columns, row))
        conn.close()

        # Création du PDF avec chemin dans le dossier dédié
        today_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"Bilan_Technique_{today_str}.pdf"
        pdf_path = os.path.join(REPORTS_DIR, filename)  # Store in reports directory
        
        c = canvas.Canvas(pdf_path, pagesize=A4)  # Changed to use pdf_path
        width, height = A4

        # --- EN-TÊTE PROFESSIONNEL --- 
        # (EXACTLY THE SAME AS YOUR ORIGINAL CODE)
        try:
            logo_path = "OCP_logo.png"
            if os.path.exists(logo_path):
                logo = ImageReader(logo_path)
                c.drawImage(logo, 50, height-100, width=100, height=80, preserveAspectRatio=True)
        except:
            pass

        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width/2, height-80, "ATELIER MCP @ MAROC CHIMIE")
        c.drawCentredString(width/2, height-105, "BILAN TECHNIQUE DES ACTIVITES")
        c.drawCentredString(width/2, height-130, "SYNTHESE DES RESULTATS")

        date_str = data.get('date', datetime.now().strftime("%Y-%m-%d"))
        c.setFont("Helvetica", 14)
        c.drawCentredString(width/2, height-160, f"Date: {date_str}")
        c.line(50, height-170, width-50, height-170)

        # --- DONNÉES ORGANISÉES ---
        y_position = height - 200
        c.setFont("Helvetica", 12)

        sections = {
            "RÉCEPTIONS": ["ca_co3_recep", "p2o5_recep", "h3po4_recep", "fuel_recep",
                          "big_bag_recep", "ffs_recep", "cp6_recep", "housse_recep"],
            "CONSOMMATIONS": ["ca_co3_cons", "p2o5_cons", "fuel_cons"],
            "PRODUCTION": ["prod_ffs", "prod_big_bag"],
            "STOCKS": ["stock_debut", "stock_fin"],
            "ARRÊTS": ["arret_externe", "arret_endogene", "arret_programme"],
            "RENDEMENTS": ["conso_specifique", "rendement"],
            "EMBALLAGE": ["bobine_utilisee", "housse_utilisee"]
        }

        for section, fields in sections.items():
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y_position, section)
            y_position -= 20
            
            c.setFont("Helvetica", 10)
            for field in fields:
                if field in data and data[field] not in (None, "", "None"):
                    field_name = field.replace("_", " ").upper()
                    c.drawString(70, y_position, f"{field_name}: {data[field]}")
                    y_position -= 15
            
            y_position -= 10
            
            if y_position < 100:
                c.showPage()
                y_position = height - 50

        c.save()
        
        # Clean up old reports
        clean_old_reports()
        
        return os.path.abspath(pdf_path)  # Return absolute path to the PDF
        
    except Exception as e:
        print(f"Erreur lors de la génération du PDF: {str(e)}")
        return False

def clean_old_reports():
    """Keep only the most recent MAX_REPORTS files"""
    try:
        files = [os.path.join(REPORTS_DIR, f) for f in os.listdir(REPORTS_DIR) 
                if f.endswith('.pdf')]
        files.sort(key=os.path.getmtime)
        
        while len(files) > MAX_REPORTS:
            os.remove(files[0])
            files.pop(0)
    except Exception as e:
        print(f"Error cleaning reports: {e}")