# pdf_generator.py

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import sqlite3
from datetime import date

def generate_pdf_from_db(db_path='data.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    today_str = date.today().strftime("%Y-%m-%d")
    cursor.execute("SELECT * FROM suivi_journalier WHERE date = ?", (today_str,))
    row = cursor.fetchone()

    if not row:
        return False  # no data

    # Fetch column names
    cursor.execute("PRAGMA table_info(suivi_journalier)")
    columns = [info[1] for info in cursor.fetchall()]
    conn.close()

    data = dict(zip(columns, row))
    
    filename = f"bilan_{today_str}.pdf"
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 50, f"Bilan du {today_str}")

    y = height - 100
    c.setFont("Helvetica", 12)

    for key, value in data.items():
        c.drawString(100, y, f"{key.replace('_', ' ').capitalize()} : {value}")
        y -= 20
        if y < 100:
            c.showPage()
            y = height - 100

    c.save()
    return True
