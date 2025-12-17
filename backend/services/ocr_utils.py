# services/ocr_utils.py
import re
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from pathlib import Path
from services.crm_api import get_customer_kyc

# ✅ FORCE POPPLER PATH (Windows)
POPPLER_PATH = r"C:\poppler\poppler-23.08.0\Library\bin"
def _normalize_name(name: str) -> str:
    """Strips leading/trailing non-alphanumeric characters and excessive spaces."""
    # 1. Strip leading/trailing non-word characters and whitespace (e.g., '-', ' ', '*')
    # This specifically targets the issue where OCR adds symbols like '-' or quotes.
    cleaned_name = re.sub(r'^\W+|\W+$', '', name.strip())
    # 2. Normalize internal whitespace to single spaces
    cleaned_name = re.sub(r'\s+', ' ', cleaned_name)
    return cleaned_name.lower()


def extract_name_from_text(text: str) -> str:
    """Extract name from text (simple heuristic) and return it in a cleaned format."""
    lines = text.split("\n")
    for line in lines:
        line = line.strip()
        # Basic heuristic: contains at least two words and no digits
        if len(line.split()) >= 2 and not any(char.isdigit() for char in line):
            # Apply initial cleaning and return in Title Case
            return _normalize_name(line).title()
    return ""

def extract_text_from_image(image_path: Path) -> str:
    img = Image.open(image_path)
    return pytesseract.image_to_string(img)


def extract_text_from_pdf(pdf_path: Path) -> str:
    pages = convert_from_path(
        pdf_path,
        dpi=300,
        poppler_path=POPPLER_PATH
    )
    # Read only first page (salary slip / PAN usually first page)
    return pytesseract.image_to_string(pages[0])


def extract_salary_from_text(text: str) -> float:
    text = text.replace(",", "")
    matches = re.findall(
        r"(?:₹|Rs\.?|INR)?\s?(\d{4,7})",
        text,
        re.IGNORECASE
    )
    if not matches:
        return 0.0
    return float(max(map(int, matches)))


def extract_salary_from_slip(file_path: Path) -> tuple[float, str]:
    """Return salary extracted from the slip and a short status message."""
    suffix = file_path.suffix.lower()

    if suffix in [".jpg", ".jpeg", ".png"]:
        text = extract_text_from_image(file_path)
    elif suffix == ".pdf":
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
        cust = cust[0]
    elif not isinstance(cust, dict):
        return {"status": "error", "message": "Invalid customer data format."}

    salary, msg = extract_salary_from_slip(file_path)
    registered_salary = cust.get("salary", 0)

    print(f"[DEBUG] OCR Extracted Salary: {salary}")
    print(f"[DEBUG] CRM Registered Salary: {registered_salary}")

    if salary == 0:
        return {"status": "error", "message": msg}

    if abs(salary - registered_salary) <= 1000:
        return {
            "status": "success",
            "message": f"✅ Salary slip verified successfully for {customer_name}."
        }

    return {
        "status": "error",
        "message": f"❌ Salary mismatch. OCR: ₹{salary}, Registered: ₹{registered_salary}."
    }


def extract_pan_from_text(text: str) -> str:
    """Extract PAN number from text (format: AAAAA9999A)."""
    match = re.search(r"\b([A-Z]{5}[0-9]{4}[A-Z])\b", text)
    return match.group(1) if match else ""


def extract_aadhaar_from_text(text: str) -> str:
    """Extract Aadhaar number from text (12 digits), removing all spaces."""
    # Pattern looks for 12 digits, optionally separated by spaces
    match = re.search(r"\b(\d{4}\s?\d{4}\s?\d{4})\b", text)
    # Return the match with all spaces removed
    return match.group(1).replace(" ", "") if match else ""


def extract_from_card(file_path: Path) -> str:
    """Extract text from image or PDF."""
    suffix = file_path.suffix.lower()

    if suffix in [".jpg", ".jpeg", ".png"]:
        return extract_text_from_image(file_path)
    elif suffix == ".pdf":
        return extract_text_from_pdf(file_path)

    return ""

def normalize_pan(pan: str) -> str:
    return pan.strip().upper().replace(" ", "")

def validate_pan_card(customer_name: str, pan_number: str, file_path: Path) -> dict:
    text = extract_from_card(file_path)
    if not text:
        return {"status": "error", "message": "Could not extract text from PAN card."}

    extracted_pan = extract_pan_from_text(text)

    if not extracted_pan:
        return {"status": "error", "message": "PAN number not found on card."}

    extracted_pan_clean = normalize_pan(extracted_pan)
    pan_number_clean = normalize_pan(pan_number)

    if extracted_pan_clean != pan_number_clean:
        return {
            "status": "mismatch",
            "message": f"PAN mismatch: Card has {extracted_pan_clean}, CRM has {pan_number_clean}."
        }

    return {
        "status": "success",
        "message": "PAN card verified successfully ✔️"
    }



def validate_aadhaar_card(customer_name: str, aadhaar_number: str, file_path: Path) -> dict:
    """Validate Aadhaar card: extract name and Aadhaar, compare with customer data, ignoring spaces in numbers and cleaning names."""
    text = extract_from_card(file_path)
    if not text:
        return {"status": "error", "message": "Could not extract text from Aadhaar card."}

    extracted_aadhaar = extract_aadhaar_from_text(text)
    extracted_name = extract_name_from_text(text)

    # Normalize BOTH numbers and names for accurate comparison
    normalized_crm_aadhaar = aadhaar_number.replace(" ", "")
    normalized_crm_name = _normalize_name(customer_name)
    normalized_extracted_name = _normalize_name(extracted_name)
    
    if not extracted_aadhaar:
        return {"status": "error", "message": "Aadhaar number not found on card."}

    # 1. Aadhaar Number Comparison (Already correct from previous fix)
    if extracted_aadhaar != normalized_crm_aadhaar:
        return {
            "status": "mismatch",
            "message": f"Aadhaar mismatch: Card has {extracted_aadhaar}, CRM has {aadhaar_number}. Please try uploading a clear document again."
        }

    # 2. Name Comparison (FIXED: Comparing cleaned versions)
    if normalized_extracted_name != normalized_crm_name:
        return {
            "status": "mismatch",
            "message": f"Name mismatch: Card has '{extracted_name}', CRM has '{customer_name}'. Please try uploading a clear document again."
        }

    return {"status": "success", "message": "Aadhaar card verified successfully."}