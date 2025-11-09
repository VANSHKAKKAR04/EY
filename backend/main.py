from fastapi import FastAPI, Request
from agents.sales_agent import SalesAgent
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ Allow your frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:5173"] for Vite
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sales_agent = SalesAgent()

@app.post("/sales")
async def handle_sales(request: Request):
    data = await request.json()
    msg = data.get("message", "")
    response = sales_agent.handle_sales(msg)
    return {"response": response}
