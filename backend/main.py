from fastapi import FastAPI, Request, UploadFile, File, Path as FPath
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles  # <--- ADD THIS LINE
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
app.mount("/sanctions", StaticFiles(directory=SANCTION_DIR), name="sanctions")

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

    # Ensure consistent keys for frontend, including NEW flags
    if isinstance(response, dict):
        return {
            "message": response.get("response", str(response)),
            "stage": response.get("stage", master_agent.state["stage"]),
            "awaitingSalarySlip": response.get("awaitingSalarySlip", False),
            "awaitingPan": response.get("awaitingPan", False),        # <-- NEW
            "awaitingAadhaar": response.get("awaitingAadhaar", False),  # <-- NEW
            "file": response.get("file"),  # optional PDF filename
        }

    # fallback for plain string
    return {
        "message": str(response),
        "stage": master_agent.state["stage"],
        "awaitingSalarySlip": False,
        "awaitingPan": False,
        "awaitingAadhaar": False,
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


# ============================================================
# 🟩 SALARY SLIP UPLOAD ENDPOINT
# ============================================================
@app.post("/upload-salary-slip")
async def upload_salary_slip(file: UploadFile = File(...)):

    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    print(f"[DEBUG] Salary slip uploaded: {file_path}")

    # Update agent state
    result = master_agent.handle_file_upload(str(file_path))

    # Ensure consistent keys for frontend
    return {
        "message": result.get("response", "Upload complete"),
        "stage": result.get("stage", master_agent.state["stage"]),
        "awaitingSalarySlip": result.get("awaitingSalarySlip", False),
        "awaitingPan": result.get("awaitingPan", False),
        "awaitingAadhaar": result.get("awaitingAadhaar", False),
        "file": result.get("file"),
    }


# ============================================================
# 🟥 PAN CARD UPLOAD ENDPOINT (Delegated to MasterAgent)
# ============================================================
@app.post("/upload-pan")
# NOTE: The customer_id parameter should ideally be included in the File request
# if the frontend handles it, but for simplicity, we rely on the MasterAgent
# having stored the customer context from previous messages.
async def upload_pan_card(file: UploadFile = File(...)):
    
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    print(f"[DEBUG] PAN card uploaded: {file_path}")

    # Delegate file validation and state transition to MasterAgent
    result = master_agent.handle_file_upload(str(file_path))

    return {
        "message": result.get("response", "Upload complete"),
        "stage": result.get("stage", master_agent.state["stage"]),
        "awaitingSalarySlip": result.get("awaitingSalarySlip", False),
        "awaitingPan": result.get("awaitingPan", False),
        "awaitingAadhaar": result.get("awaitingAadhaar", False),
        "file": result.get("file"),
    }


# ============================================================
# 🟧 AADHAAR CARD UPLOAD ENDPOINT (Delegated to MasterAgent)
# ============================================================
@app.post("/upload-aadhaar")
# NOTE: Removed customer_id parameter for delegation simplicity
async def upload_aadhaar_card(file: UploadFile = File(...)):
    
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    print(f"[DEBUG] Aadhaar card uploaded: {file_path}")

    # Delegate file validation and state transition to MasterAgent
    result = master_agent.handle_file_upload(str(file_path))

    return {
        "message": result.get("response", "Upload complete"),
        "stage": result.get("stage", master_agent.state["stage"]),
        "awaitingSalarySlip": result.get("awaitingSalarySlip", False),
        "awaitingPan": result.get("awaitingPan", False),
        "awaitingAadhaar": result.get("awaitingAadhaar", False),
        "file": result.get("file"),
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