from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
from pathlib import Path

def generate_sanction_pdf(name: str, amount: float, rate: float, tenure: int, credit_score: int = None):
    """
    Generates a formal Tata Capital personal loan sanction letter as a PDF.
    """
    # Folder for generated letters
    output_dir = Path("sanctions")
    output_dir.mkdir(parents=True, exist_ok=True)
    file_path = output_dir / f"sanction_{name.replace(' ', '_')}.pdf"

    # Create PDF
    c = canvas.Canvas(str(file_path), pagesize=A4)
    width, height = A4

    # Header
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width / 2, 800, "TATA CAPITAL - PERSONAL LOAN SANCTION LETTER")

    # Metadata
    c.setFont("Helvetica", 10)
    c.drawRightString(550, 780, f"Date: {datetime.now().strftime('%d-%m-%Y')}")
    c.drawString(50, 780, f"Ref No: TCPL-{str(hash(name))[:6].upper()}")

    # Customer details
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 740, "To,")
    c.setFont("Helvetica", 12)
    c.drawString(50, 725, f"{name}")
    c.drawString(50, 710, "Subject: Loan Sanction Approval")

    # Loan details
    emi = calculate_emi(amount, rate, tenure)
    c.setFont("Helvetica", 12)
    text = c.beginText(50, 680)
    text.textLines(f"""
Dear {name},

We are pleased to inform you that your personal loan request has been approved based on
successful KYC and credit evaluation.

Loan Details:
    • Sanctioned Loan Amount: ₹{amount:,.2f}
    • Interest Rate: {rate:.2f}% p.a.
    • Tenure: {tenure} years
    • Approx. EMI: ₹{emi:,.2f}
    • Credit Score: {credit_score if credit_score else 'Not available'}

Please note this offer is subject to standard Tata Capital terms and conditions.

Warm regards,
Tata Capital Loan Department
    """)
    c.drawText(text)

    # Footer
    c.setFont("Helvetica-Oblique", 10)
    c.drawCentredString(width / 2, 60, "This is a system-generated document and does not require a physical signature.")

    c.save()
    return str(file_path)

def calculate_emi(principal: float, annual_rate: float, years: int) -> float:
    r = annual_rate / (12 * 100)
    n = years * 12
    if r == 0:
        return principal / n
    emi = principal * r * ((1 + r) ** n) / ((1 + r) ** n - 1)
    return emi
