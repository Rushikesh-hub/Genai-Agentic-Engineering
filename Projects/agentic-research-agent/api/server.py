import uuid
from fastapi import FastAPI
from pydantic import BaseModel

from agent.dynamic_orchestrator import run_dynamic_system

# -----------------------------
# App Setup
# -----------------------------

app = FastAPI(
    title="Agentic AI API",
    description="Dynamic Multi-Agent + RAG System",
    version="1.0"
)


# -----------------------------
# Session Memory (simple version)
# -----------------------------

sessions = {}

# -----------------------------
# Request Schema
# -----------------------------

class ChatRequest(BaseModel):
    message: str
    session_id: str = None


# -----------------------------
# Health Check
# -----------------------------

@app.get("/")
def home():
    return {"status": "Agent API running"}


# -----------------------------
# Chat Endpoint
# -----------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    # Generate session if not provided
    if not request.session_id:
        session_id = str(uuid.uuid4())
        sessions[session_id] = []
    else:
        session_id = request.session_id
        sessions.setdefault(session_id, [])

    # Add user message
    sessions[session_id].append({"role": "user", "content": request.message})

    # Run agent system
    response = run_dynamic_system(request.message)

    # Store response
    sessions[session_id].append({"role": "assistant", "content": response})

    return {
        "session_id": session_id,
        "response": response
    }