from fastapi import FastAPI, UploadFile, File, Path as FPath
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from routers.crm import router as crm_router
from routers.offer_mart import router as offer_mart_router
from services.crm_api import get_customer_by_id
from agents.master_agent import MasterAgent

from pathlib import Path
import shutil
from pydantic import BaseModel
from typing import Optional, Dict

# ============================================================
# 🚀 APP INITIALIZATION
# ============================================================

app = FastAPI(title="Loan Assistant Backend")

# ============================================================
# 🌐 CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ey-front.onrender.com",
        "http://localhost:5173",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# 📦 ROUTERS
# ============================================================

app.include_router(crm_router)
app.include_router(offer_mart_router)

# ============================================================
# 🧠 SINGLE GLOBAL AGENT (NO SESSIONS)
# ============================================================

agent = MasterAgent()

# ============================================================
# 💾 STORAGE
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
SANCTION_DIR = BASE_DIR / "sanctions"

UPLOAD_DIR.mkdir(exist_ok=True)
SANCTION_DIR.mkdir(exist_ok=True)

# ============================================================
# 📄 STATIC SANCTION FILES
# ============================================================

app.mount("/sanctions", StaticFiles(directory=SANCTION_DIR), name="sanctions")

# ============================================================
# 💬 CHAT API
# ============================================================

class ChatRequest(BaseModel):
    message: str
    customer: Optional[Dict] = None


@app.post("/chat")
async def handle_chat(payload: ChatRequest):
    response = agent.handle_message(
        payload.message,
        payload.customer
    )

    return {
        "message": response.get("response"),
        "stage": response.get("stage"),
        "awaitingSalarySlip": response.get("awaitingSalarySlip", False),
        "awaitingPan": response.get("awaitingPan", False),
        "awaitingAadhaar": response.get("awaitingAadhaar", False),
        "file": response.get("file"),
    }

# ============================================================
# 👤 CUSTOMER PROFILE
# ============================================================

@app.get("/profile/{customer_id}")
async def get_customer_profile(customer_id: int):
    customer = get_customer_by_id(customer_id)
    if not customer:
        return {"error": "Customer not found"}

    safe = dict(customer)
    safe.pop("password_hash", None)
    return safe

# ============================================================
# 📤 FILE UPLOAD HELPERS
# ============================================================

def save_and_process_file(file: UploadFile):
    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return agent.handle_file_upload(str(file_path))

# ============================================================
# 📎 FILE UPLOAD ENDPOINTS
# ============================================================

@app.post("/upload-pan")
async def upload_pan(file: UploadFile = File(...)):
    return save_and_process_file(file)


@app.post("/upload-aadhaar")
async def upload_aadhaar(file: UploadFile = File(...)):
    return save_and_process_file(file)


@app.post("/upload-salary-slip")
async def upload_salary_slip(file: UploadFile = File(...)):
    return save_and_process_file(file)

# ============================================================
# 📥 DOWNLOAD SANCTION LETTER
# ============================================================

@app.get("/download-sanction/{filename}")
async def download_sanction_letter(filename: str = FPath(...)):
    file_path = SANCTION_DIR / filename

    if not file_path.exists():
        return {"error": "File not found"}

    return FileResponse(
        path=file_path,
        filename=file_path.name,
        media_type="application/pdf",
    )
