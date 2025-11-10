from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from agents.master_agent import MasterAgent

app = FastAPI()

# ✅ Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Create one master agent for the entire app
master_agent = MasterAgent()

@app.post("/chat")
async def handle_chat(request: Request):
    data = await request.json()
    msg = data.get("message", "")
    response = master_agent.handle_message(msg)
    return {"response": response}
