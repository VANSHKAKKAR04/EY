from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
from pathlib import Path


def generate_sanction_pdf(
    name: str,
    loan_type: str,
    amount: float,
    rate: float,
    tenure: int,
    credit_score: int = None
):
    """
    Generates a formal FinWise (Tata Capital) loan sanction letter as a PDF,
    clearly displaying the loan type selected during sales.
    """

    # Folder for generated letters
    output_dir = Path("sanctions")
    output_dir.mkdir(parents=True, exist_ok=True)
    file_path = output_dir / f"sanction_{name.replace(' ', '_')}.pdf"

    # Create PDF
    c = canvas.Canvas(str(file_path), pagesize=A4)
    width, height = A4

    loan_type_title = loan_type.upper()

    # --------------------------------------------------
    # Header
    # --------------------------------------------------
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(
        width / 2,
        800,
        f"FinWise - {loan_type_title} LOAN SANCTION LETTER"
    )

    # Metadata
    c.setFont("Helvetica", 10)
    c.drawRightString(550, 780, f"Date: {datetime.now().strftime('%d-%m-%Y')}")
    c.drawString(50, 780, f"Ref No: TCPL-{str(abs(hash(name)))[:6].upper()}")

    # --------------------------------------------------
    # Customer Details
    # --------------------------------------------------
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 740, "To,")
    c.setFont("Helvetica", 12)
    c.drawString(50, 725, name)
    c.drawString(
        50,
        710,
        f"Subject: {loan_type_title} Loan Sanction Approval"
    )

    # --------------------------------------------------
    # Loan Details
    # --------------------------------------------------
    emi = calculate_emi(amount, rate, tenure)

    c.setFont("Helvetica", 12)
    text = c.beginText(50, 675)
    text.setLeading(18)

    text.textLine(f"Dear {name},")
    text.textLine("")
    text.textLine(
        f"We are pleased to inform you that your {loan_type} loan request "
        "has been approved based on successful KYC and credit evaluation."
    )
    text.textLine("")
    text.textLine("Loan Details:")
    text.textLine(f"    • Loan Type           : {loan_type_title} Loan")
    text.textLine(f"    • Sanctioned Amount   : ₹{amount:,.2f}")
    text.textLine(f"    • Interest Rate       : {rate:.2f}% p.a.")
    text.textLine(f"    • Tenure              : {tenure} years")
    text.textLine(f"    • Approx. EMI         : ₹{emi:,.2f}")
    text.textLine(
        f"    • Credit Score        : {credit_score if credit_score else 'Not available'}"
    )
    text.textLine("")
    text.textLine(
        "Please note that this sanction is subject to FinWise (Tata Capital) "
        "standard terms and conditions."
    )
    text.textLine("")
    text.textLine("Warm regards,")
    text.textLine("FinWise")
    text.textLine("Tata Capital Loan Department")

    c.drawText(text)

    # --------------------------------------------------
    # Footer
    # --------------------------------------------------
    c.setFont("Helvetica-Oblique", 10)
    c.drawCentredString(
        width / 2,
        60,
        "This is a system-generated document and does not require a physical signature."
    )

    c.save()
    return str(file_path)


def calculate_emi(principal: float, annual_rate: float, years: int) -> float:
    r = annual_rate / (12 * 100)
    n = years * 12

    if r == 0:
        return principal / n

    emi = principal * r * ((1 + r) ** n) / ((1 + r) ** n - 1)
    return emi
