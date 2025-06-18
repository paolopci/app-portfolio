import pandas as pd
import glob
import os
from fpdf import FPDF
from pathlib import Path

# Trova tutti i file .xlsx nella cartella invoices
file_paths = glob.glob("invoices/*.xlsx")


class PDF(FPDF):
    pass


# Itera su ciascun file Excel
for index, file in enumerate(file_paths, start=1):
    try:
        df = pd.read_excel(file, sheet_name="Sheet 1")
    except Exception as e:
        print(f"Errore nella lettura di {file}: {e}")
        continue

    pdf = PDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    # ho una stringa che rappresenta il nome del file. es ."100001-2023-2-18"
    filename = Path(file).stem
    invoice_nr, invoice_data = filename.split("-")

    pdf.set_font("Arial", size=10)
    pdf.cell(w=100, h=8, txt=f"Invoice nr. {invoice_nr}", ln=1)
    pdf.cell(w=100, h=8, txt=f"Invoice Date: {invoice_data}", ln=1)
    pdf.ln(4)
    # genero i pdf in una sottocartella pdf/
    output_name = os.path.join("invoices/pdf/", f"{filename}.pdf")

    col_width = 190 / len(df.columns)
    row_height = 8

    # Intestazioni colonna
    for col_name in df.columns:
        pdf.cell(col_width, row_height, col_name, border=1)
    pdf.ln(row_height)

    # Contenuto tabellare con wrapping manuale
    for _, row in df.iterrows():
        x_start = pdf.get_x()
        y_start = pdf.get_y()
        cell_lines = []
        max_lines = 1

        # Calcolo quante linee servono per ogni colonna
        for item in row:
            text = str(item)
            words = text.split()
            line = ""
            lines = []
            for word in words:
                if pdf.get_string_width(line + " " + word) < col_width:
                    line += " " + word if line else word
                else:
                    lines.append(line)
                    line = word
            if line:
                lines.append(line)
            cell_lines.append(lines)
            max_lines = max(max_lines, len(lines))

        # Scrittura effettiva delle celle
        for line_idx in range(max_lines):
            for i, lines in enumerate(cell_lines):
                txt = lines[line_idx] if line_idx < len(lines) else ""
                pdf.cell(col_width, row_height, txt, border=1)
            pdf.ln(row_height)

    pdf.output(output_name)
    print(f"Creato PDF: {output_name}")
