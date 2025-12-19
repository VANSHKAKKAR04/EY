from fastapi import FastAPI, Request, UploadFile, File, Path as FPath
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from routers.crm import router as crm_router
from routers.offer_mart import router as offer_mart_router
from services.crm_api import get_customer_by_id
from services.session_manager import SessionManager

from pathlib import Path
import shutil
from pydantic import BaseModel
from typing import Optional, Dict



# ============================================================
# 🚀 APP INITIALIZATION
# ============================================================

app = FastAPI(title="Loan Assistant Backend")

# ============================================================
# 🌐 CORS (CRITICAL)
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ey-front.onrender.com",  # frontend domain
        "http://localhost:5173",          # local dev
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
# 🧠 SESSION MANAGER
# ============================================================

session_manager = SessionManager()

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
    session_id: Optional[str] = None

@app.post("/chat")
async def handle_chat(payload: ChatRequest):
    # data = await request.json()
    try:
        msg = payload.message
        customer = payload.customer
        session_id = payload.session_id

        print(f"Received message: {msg} {customer} {session_id}")
    
        if not session_id:
            session_id = session_manager.create_session()

        print(f"Using session ID: {session_id}")

        agent = session_manager.get_agent(session_id)
        print(f"Agent retrieved for session ID: {agent}")
        response = agent.handle_message(msg, user_profile=customer)
        print(f"Response from agent: {response}")

        return {
            "session_id": session_id,
            "message": response.get("response"),
            "stage": response.get("stage"),
            "awaitingSalarySlip": response.get("awaitingSalarySlip", False),
            "awaitingPan": response.get("awaitingPan", False),
            "awaitingAadhaar": response.get("awaitingAadhaar", False),
            "file": response.get("file"),
        }
    except:
        return {"error": "An error occurred while processing the chat message.", "session_id": session_id}


    

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

def save_and_process_file(session_id: str, file: UploadFile):
    agent = session_manager.get_agent(session_id)

    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return agent.handle_file_upload(str(file_path))


@app.post("/upload-salary-slip")
async def upload_salary_slip(session_id: str, file: UploadFile = File(...)):
    return save_and_process_file(session_id, file)


@app.post("/upload-pan")
async def upload_pan(session_id: str, file: UploadFile = File(...)):
    return save_and_process_file(session_id, file)


@app.post("/upload-aadhaar")
async def upload_aadhaar(session_id: str, file: UploadFile = File(...)):
    return save_and_process_file(session_id, file)

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
