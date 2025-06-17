from fpdf import FPDF
import pandas as pd
# This is a simple example of how to create a PDF file using the FPDF library in Python.

# leggo il file topics.csv
df = pd.read_csv('topics.csv')


pdf = FPDF(orientation='P', unit='mm', format='A4')


for index, row in df.iterrows():
    # Add a new page for each topic
    icount = 0
    while icount < int(row['Pages']):
        pdf.add_page()
        # Set font for the topic title
        pdf.set_font("Arial", size=16, style='B')
        pdf.set_text_color(254, 0, 0)  # Red color for the title
        # Add a cell with the topic title
        pdf.cell(w=0, h=10, txt=row['Topic'], align='L', ln=1)
        pdf.line(10, 20, 200, 20)  # Draw a line under the title
        icount += 1


# generate a pdf
pdf.output('output.pdf')
