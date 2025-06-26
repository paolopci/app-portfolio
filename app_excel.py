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
    filename = Path(file).stem
    invoice_nr, invoice_data = filename.split("-")

    pdf.set_font("Arial", style="B", size=10)
    pdf.cell(w=100, h=8, txt=f"Invoice nr. {invoice_nr}", ln=1)
    pdf.cell(w=100, h=8, txt=f"Invoice Date: {invoice_data}", ln=1)
    pdf.ln(4)

    output_name = os.path.join("invoices/pdf/", f"{filename}.pdf")

    col_width = 190 / len(df.columns)
    row_height = 8
    totale_fattura = 0

    # Intestazioni in grassetto
    pdf.set_font("Arial", style="B", size=10)
    for col_name in df.columns:
        label = col_name.replace("_", " ").title()
        pdf.cell(col_width, row_height, label, border=1)
    pdf.ln(row_height)

    pdf.set_font("Arial", size=10)
    for _, row in df.iterrows():
        totale_fattura += float(row.iloc[4])
        x_start = pdf.get_x()
        y_start = pdf.get_y()
        cell_lines = []
        max_lines = 1

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

        for line_idx in range(max_lines):
            for i, lines in enumerate(cell_lines):
                txt = lines[line_idx] if line_idx < len(lines) else ""
                pdf.cell(col_width, row_height, txt, border=1)
            pdf.ln(row_height)

    # Aggiunta riga finale con "Totale"
    empty_row = ["" for _ in df.columns]
    col_names = [col.lower().strip() for col in df.columns]
    try:
        idx_price_unit = col_names.index("price_per_unit")
        idx_total_price = col_names.index("total_price")
    except ValueError as e:
        print(f"Errore nel trovare le colonne: {e}")
        continue

    empty_row[idx_price_unit] = "Totale"
    empty_row[idx_total_price] = f"{totale_fattura:.2f}"

    pdf.set_font("Arial", style="B", size=10)
    for item in empty_row:
        pdf.cell(col_width, row_height, str(item), border=1)
    pdf.ln(row_height)

    # Testo sotto la tabella
    pdf.set_font("Arial", style="B", size=10)
    pdf.cell(
        w=190, h=8, txt=f"The total amount is {totale_fattura:.2f} EUR", ln=1)
    pdf.cell(w=190, h=8, txt="PythonHow", ln=1)

    print(f"totale fattura: {totale_fattura}")
    print("--------------------------------------------------------")

    pdf.output(output_name)
    print(f"Creato PDF: {output_name}")
