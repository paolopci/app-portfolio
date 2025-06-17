from fpdf import FPDF
import pandas as pd
# This is a simple example of how to create a PDF file using the FPDF library in Python.

# leggo il file topics.csv
df = pd.read_csv('topics.csv')

pdf = FPDF(orientation='P', unit='mm', format='A4')

for index, row in df.iterrows():
    # Add pages for each topic
    for page_num in range(int(row['Pages'])):
        pdf.add_page()

        # Set font for the topic title
        pdf.set_font("Arial", size=16, style='B')
        pdf.set_text_color(254, 0, 0)  # Red color for the title

        # Add a cell with the topic title
        pdf.cell(w=0, h=10, txt=row['Topic'], align='L', ln=1)

        # Draw a line under the title
        pdf.line(10, 20, 200, 20)

        # Footer - Draw line at bottom (più in alto per essere visibile)
        pdf.line(10, 270, 200, 270)

        # Add page number in footer
        pdf.set_font("Arial", size=10)
        pdf.set_text_color(0, 0, 0)  # Black color for page number
        pdf.set_xy(10, 270)  # Position below the footer line
        pdf.cell(0, 5, f"Pagina {pdf.page_no()}", align='R')

# generate a pdf
pdf.output('output.pdf')
