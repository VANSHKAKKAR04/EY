from utils.pdf_generator import generate_sanction_pdf

class SanctionAgent:
    def generate_letter(self):
        file_path = generate_sanction_pdf("Ravi Kumar", 500000, 10.5, 3)
        return f"Loan sanctioned! PDF generated: {file_path}"
