from fastapi import FastAPI, Request, UploadFile, File, Path as FPath
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from routers.crm import router as crm_router
from routers.offer_mart import router as offer_mart_router
from services.crm_api import get_customer_by_id
from services.session_manager import SessionManager

from pathlib import Path
import shutil

# ============================================================
# 🚀 APP INITIALIZATION
# ============================================================
app = FastAPI(title="Loan Assistant Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# 📦 ROUTERS (MUST COME FIRST)
# ============================================================
app.include_router(crm_router)
app.include_router(offer_mart_router)

# ============================================================
# 🧠 SESSION MANAGER
# ============================================================
session_manager = SessionManager()

# ============================================================
# 💾 PERSISTENT STORAGE (Render-safe)
# ============================================================

BASE_DIR = Path(__file__).resolve().parent  # backend/
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = BASE_DIR / "uploads"
SANCTION_DIR = BASE_DIR/"sanctions"

UPLOAD_DIR.mkdir(exist_ok=True)
SANCTION_DIR.mkdir(exist_ok=True)

# Serve sanction PDFs
app.mount("/sanctions", StaticFiles(directory=SANCTION_DIR), name="sanctions")

# ============================================================
# 🟦 CHAT ENDPOINT
# ============================================================
@app.post("/chat")
async def handle_chat(request: Request):
    data = await request.json()
    msg = data.get("message", "")
    customer = data.get("customer")
    session_id = data.get("session_id")

    if not session_id:
        session_id = session_manager.create_session()

    agent = session_manager.get_agent(session_id)
    response = agent.handle_message(msg, user_profile=customer)

    return {
        "session_id": session_id,
        "message": response.get("response"),
        "stage": response.get("stage"),
        "awaitingSalarySlip": response.get("awaitingSalarySlip", False),
        "awaitingPan": response.get("awaitingPan", False),
        "awaitingAadhaar": response.get("awaitingAadhaar", False),
        "file": response.get("file"),
    }

# ============================================================
# 🟪 GET CUSTOMER PROFILE
# ============================================================
@app.get("/profile/{customer_id}")
async def get_customer_profile(customer_id: int):
    customer = get_customer_by_id(customer_id)
    if customer:
        safe = dict(customer)
        safe.pop("password_hash", None)
        return safe
    return {"error": "Customer not found"}

# ============================================================
# 🟩 FILE UPLOAD HELPERS
# ============================================================
def save_and_process_file(session_id: str, file: UploadFile):
    agent = session_manager.get_agent(session_id)

    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return agent.handle_file_upload(str(file_path))

@app.post("/upload-salary-slip")
async def upload_salary_slip(session_id: str, file: UploadFile = File(...)):
    result = save_and_process_file(session_id, file)
    return result

@app.post("/upload-pan")
async def upload_pan(session_id: str, file: UploadFile = File(...)):
    result = save_and_process_file(session_id, file)
    return result

@app.post("/upload-aadhaar")
async def upload_aadhaar(session_id: str, file: UploadFile = File(...)):
    result = save_and_process_file(session_id, file)
    return result

# ============================================================
# 🟨 DOWNLOAD SANCTION LETTER
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

# ============================================================
# 🟧 REACT FRONTEND (LAST, GET ONLY)
# ============================================================
FRONTEND_DIR = Path(__file__).parent.parent / "frontend" / "dist"

if FRONTEND_DIR.exists():
    @app.get("/{full_path:path}", response_class=HTMLResponse)
    async def serve_react(full_path: str):
        index_file = FRONTEND_DIR / "index.html"
        if index_file.exists():
            return index_file.read_text()
        return "Frontend not built", 404
