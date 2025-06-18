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
    filename = Path(file).stem.capitalize()
    pdf.add_page()
    pdf.set_font("Arial", size=15)
    pdf.cell(w=100, h=8, txt=f"{filename}", ln=1)

output_name = os.path.join("animals/pdf/", f"animals.pdf")
pdf.output(output_name)

#  output_name = os.path.join("animals/pdf/", f"{filename}.pdf")
#     pdf.output(output_name)
# try:
#     with open(file, 'r') as f:
#         content = f.read()
#         print(f"File {index}: {content}")
#         print('')
#         print('# ----------------------------------------------')
#         print('')
# except Exception as e:
#     print(f"Error reading file {file}: {str(e)}")
