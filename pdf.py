from fpdf import FPDF

pdf=FPDF()
pdf.add_page()
pdf.set_font("Arial",size=12)
pdf.cell(200,10,txt="welcome to i knofw pythonfffffffffffffffff", ln=1,align="C")
pdf.cell(200,10,txt="here we go", ln=2,align="C")

pdf.output("1.pdf")