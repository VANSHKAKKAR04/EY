# services/ocr_utils.py
import re
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from pathlib import Path
from services.crm_api import get_customer_kyc

def extract_text_from_image(image_path: Path) -> str:
    img = Image.open(image_path)
    return pytesseract.image_to_string(img)

def extract_text_from_pdf(pdf_path: Path) -> str:
    pages = convert_from_path(pdf_path, dpi=300)
    return pytesseract.image_to_string(pages[0])

def extract_salary_from_text(text: str) -> float:
    text = text.replace(",", "")
    matches = re.findall(r"(?:₹|Rs\.?|INR)?\s?(\d{4,7})", text, re.IGNORECASE)
    if not matches:
        return 0.0
    return float(max(map(int, matches)))

def extract_salary_from_slip(file_path: Path) -> tuple[float, str]:
    """Return salary extracted from the slip and a short status message."""
    if file_path.suffix.lower() in [".jpg", ".jpeg", ".png"]:
        text = extract_text_from_image(file_path)
    elif file_path.suffix.lower() == ".pdf":
        text = extract_text_from_pdf(file_path)
    else:
        return 0.0, "❌ Unsupported file format."

    salary = extract_salary_from_text(text)
    if salary == 0:
        return 0.0, "⚠ No salary amount detected on slip."
    return salary, f"✅ Extracted salary ₹{salary:,.0f}"

def validate_salary_slip(customer_name: str, file_path: Path) -> dict:
    """Full end-to-end validation comparing OCR salary with CRM salary."""
    cust = get_customer_kyc(customer_name)
    if not cust:
        return {"status": "error", "message": f"No customer found for '{customer_name}'"}

    # Handle list vs dict
    if isinstance(cust, list):
        cust = cust[0]  # pick first record
    elif not isinstance(cust, dict):
        return {"status": "error", "message": "Invalid customer data format."}

    salary, msg = extract_salary_from_slip(file_path)
    registered_salary = cust.get("salary", 0)
    print(f"[DEBUG] OCR Extracted Salary: {salary}")
    print(f"[DEBUG] CRM Registered Salary: {registered_salary}")

    if salary == 0:
        return {"status": "error", "message": msg}

    if abs(salary - registered_salary) <= 1000:
        return {"status": "success", "message": f"✅ Salary slip verified successfully for {customer_name}."}
    else:
        return {
            "status": "mismatch",
            "message": f"⚠ Salary slip shows ₹{salary:,.0f}, but CRM has ₹{registered_salary:,.0f}. Verification required."
        }
