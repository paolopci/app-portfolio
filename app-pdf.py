from fpdf import FPDF


pdf = FPDF(orientation='P', unit='mm', format='A4')

pdf.add_page()
# Set font for the first line
pdf.set_font("Arial", size=12, style='B')
# Add a cell with the first line ln=1 --> to move to the next line
# w=0 --> to use the full width of the page, h=12 --> height of the cell
pdf.cell(w=0, h=12, txt='Hello world!', align='L', ln=1, border=1)
# Set font for the second line,style='I' --> italic
pdf.set_font("Times", size=10, style='I')
pdf.cell(0, 12, 'Hello world!', align='L', ln=1, border=1)


# generate a pdf
pdf.output('output.pdf')
