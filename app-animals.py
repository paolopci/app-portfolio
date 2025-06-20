import pandas as pd
import glob
import os
from fpdf import FPDF
from pathlib import Path


class PDF(FPDF):
    pass


file_paths = glob.glob('animals/*.txt')

pdf = PDF(orientation="P", unit="mm", format="A4")

for index, file in enumerate(file_paths, start=1):
    print(file)
    filename = Path(file).stem.capitalize()
    pdf.add_page()
    pdf.set_font("Arial", size=15)
    pdf.cell(w=100, h=8, txt=f"{filename}", ln=1)
    try:
        with open(file, "r") as f:
            content = f.read()

        pdf.set_font("Arial", size=10)
        pdf.multi_cell(w=0, h=8, txt=content)
    except Exception as e:
        print(f"Error reading file {file}: {str(e)}")


output_name = os.path.join("animals/pdf/", f"animals.pdf")
pdf.output(output_name)
