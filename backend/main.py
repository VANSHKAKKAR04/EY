from fastapi import FastAPI, Request, UploadFile, File, Path as FPath
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from agents.master_agent import MasterAgent
import shutil
from pathlib import Path

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


# ============================================================
# 🟩 SALARY SLIP UPLOAD ENDPOINT
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
