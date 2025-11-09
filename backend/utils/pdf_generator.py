from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_sanction_pdf(name, amount, rate, tenure):
    file_path = f"sanction_{name.replace(' ', '_')}.pdf"
    c = canvas.Canvas(file_path, pagesize=A4)
    c.drawString(100, 750, "TATA CAPITAL SANCTION LETTER")
    c.drawString(100, 720, f"Name: {name}")
    c.drawString(100, 700, f"Loan Amount: ₹{amount}")
    c.drawString(100, 680, f"Interest Rate: {rate}%")
    c.drawString(100, 660, f"Tenure: {tenure} years")
    c.drawString(100, 640, "Congratulations! Your personal loan is approved.")
    c.save()
    return file_path
