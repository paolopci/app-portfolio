from fpdf import FPDF
import pandas as pd

# Questo è un semplice esempio di come creare un file PDF usando la libreria FPDF
#  in Python.
df = pd.read_csv('topics.csv')

pdf = FPDF(orientation='P', unit='mm', format='A4')

for index, row in df.iterrows():
    for page_num in range(int(row['Pages'])):
        pdf.add_page()

        # Titolo
        pdf.set_font("Arial", size=16, style='B')
        pdf.set_text_color(254, 0, 0)
        pdf.cell(w=0, h=10, txt=row['Topic'], align='L', ln=1)

        # Linea sotto il titolo
        pdf.line(10, 20, 200, 20)

        # === RIGHE ORIZZONTALI OGNI 10mm ===
        # Inizia da 30mm (dopo la linea sotto il titolo) fino a 260mm
        # (prima del footer)
        for y in range(30, 270, 10):
            pdf.line(10, y, 200, y)
        # ===================================

        # Footer - Linea orizzontale in basso
        pdf.line(10, 270, 200, 270)

        # Numero pagina nel footer
        pdf.set_font("Arial", size=10)
        pdf.set_text_color(0, 0, 0)
        pdf.set_xy(10, 270)
        pdf.cell(0, 5, f"Pagina {pdf.page_no()}", align='R')

# Salva il PDF
pdf.output('output.pdf')
