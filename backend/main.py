from fastapi import FastAPI, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
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

@app.post("/chat")
async def handle_chat(request: Request):
    data = await request.json()
    msg = data.get("message", "")
    response = master_agent.handle_message(msg)
    return {"response": response, "stage": master_agent.state["stage"]}

@app.post("/upload-salary-slip")
async def upload_salary_slip(file: UploadFile = File(...)):
    """Accepts salary slip upload only during KYC stage."""
    if master_agent.state["stage"] != "kyc":
        return {"error": "❌ Salary slip can only be uploaded during KYC verification."}

    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    print(f"[DEBUG] Salary slip uploaded: {file_path}")
    return {"message": f"✅ Salary slip '{file.filename}' uploaded successfully."}
