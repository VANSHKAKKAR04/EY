from fastapi import FastAPI, Request, UploadFile, File, Path as FPath
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from agents.master_agent import MasterAgent
import shutil
from pathlib import Path
from services.crm_api import get_customer_by_id

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

master_agent = MasterAgent()
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
SANCTION_DIR = Path("sanctions")
SANCTION_DIR.mkdir(exist_ok=True)


# ============================================================
# 🟦 CHAT ENDPOINT
# ============================================================
@app.post("/chat")
async def handle_chat(request: Request):
    data = await request.json()
    msg = data.get("message", "")
    customer = data.get("customer")

    # pass optional customer profile to master agent for personalization
    response = master_agent.handle_message(msg, user_profile=customer)

    # Ensure consistent keys for frontend
    if isinstance(response, dict):
        return {
            "message": response.get("response", str(response)),
            "stage": response.get("stage", master_agent.state["stage"]),
            "awaitingSalarySlip": response.get("awaitingSalarySlip", False),
            "file": response.get("file"),  # optional PDF filename
        }

    # fallback for plain string
    return {
        "message": str(response),
        "stage": master_agent.state["stage"],
        "awaitingSalarySlip": False,
    }


# ============================================================# 🟪 GET CUSTOMER PROFILE ENDPOINT
# ============================================================
@app.get("/profile/{customer_id}")
async def get_customer_profile(customer_id: int):
    customer = get_customer_by_id(customer_id)
    if customer:
        # Remove sensitive fields
        safe = dict(customer)
        safe.pop("password_hash", None)
        return safe
    return {"error": "Customer not found"}


# ============================================================# 🟩 SALARY SLIP UPLOAD ENDPOINT
# ============================================================
@app.post("/upload-salary-slip")
async def upload_salary_slip(file: UploadFile = File(...)):

    # Save file
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    print(f"[DEBUG] Salary slip uploaded: {file_path}")

    # Update agent state
    result = master_agent.handle_file_upload(str(file_path))

    return {
        "message": result.get("response", "Upload complete"),
        "stage": result.get("stage", master_agent.state["stage"]),
        "awaitingSalarySlip": result.get("awaitingSalarySlip", False),
        "file": result.get("file"),  # optional PDF filename
    }


# ============================================================
# 🟥 PAN CARD UPLOAD ENDPOINT
# ============================================================
@app.post("/upload-pan")
async def upload_pan_card(customer_id: int, file: UploadFile = File(...)):
    from services.ocr_utils import validate_pan_card
    from services.crm_api import get_customer_by_id

    customer = get_customer_by_id(customer_id)
    if not customer:
        return {"error": "Customer not found"}

    # Save file
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    print(f"[DEBUG] PAN card uploaded: {file_path}")

    # Validate PAN card
    result = validate_pan_card(customer["name"], customer["pan_number"], file_path)

    if result["status"] == "success":
        return {
            "message": result["message"] + "\n\n📄 Please upload your Aadhaar card for validation.",
            "stage": "kyc_collect",
            "awaitingPan": False,
            "awaitingAadhaar": True,
            "awaitingSalarySlip": False,
        }
    else:
        return {
            "message": result["message"],
            "stage": "kyc_collect",
            "awaitingPan": True,
            "awaitingAadhaar": False,
            "awaitingSalarySlip": False,
        }


# ============================================================
# 🟧 AADHAAR CARD UPLOAD ENDPOINT
# ============================================================
@app.post("/upload-aadhaar")
async def upload_aadhaar_card(customer_id: int, file: UploadFile = File(...)):
    from services.ocr_utils import validate_aadhaar_card
    from services.crm_api import get_customer_by_id

    customer = get_customer_by_id(customer_id)
    if not customer:
        return {"error": "Customer not found"}

    # Save file
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    print(f"[DEBUG] Aadhaar card uploaded: {file_path}")

    # Validate Aadhaar card
    result = validate_aadhaar_card(customer["name"], customer["aadhaar_number"], file_path)

    if result["status"] == "success":
        # KYC complete, go to underwriting
        underwriting_message = "🎉 KYC Completed Successfully!\n\nProceeding with loan evaluation..."
        return {
            "message": result["message"] + "\n\n" + underwriting_message,
            "stage": "underwriting",
            "awaitingPan": False,
            "awaitingAadhaar": False,
            "awaitingSalarySlip": False,  # Assuming no salary slip needed
        }
    else:
        return {
            "message": result["message"],
            "stage": "kyc_collect",
            "awaitingPan": False,
            "awaitingAadhaar": True,
            "awaitingSalarySlip": False,
        }


# ============================================================
# 🟨 DOWNLOAD SANCTION LETTER ENDPOINT
# ============================================================
@app.get("/download-sanction/{filename}")
async def download_sanction_letter(filename: str = FPath(...)):
    file_path = SANCTION_DIR / filename

    if not file_path.exists():
        return {"error": "File not found."}

    return FileResponse(
        path=file_path,
        filename=file_path.name,
        media_type="application/pdf"
    )
