import uuid
import asyncio
import logging

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from agent.dynamic_orchestrator import run_dynamic_system

# -----------------------------
# Logging Setup
# -----------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# -----------------------------
# FastAPI App
# -----------------------------

app = FastAPI(
    title="Agentic AI API",
    description="Dynamic Multi-Agent + RAG + Memory + Streaming",
    version="2.0"
)

# -----------------------------
# Session Store (In-Memory)
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
def health():
    return {
        "status": "running",
        "service": "Agentic AI API with Streaming"
    }


# -----------------------------
# Utility: Create/Get Session
# -----------------------------

def get_session(session_id):

    if not session_id:
        session_id = str(uuid.uuid4())
        sessions[session_id] = []
    else:
        sessions.setdefault(session_id, [])

    return session_id


# -----------------------------
# Streaming Generator
# -----------------------------

async def stream_response(text: str):
    """
    Simulated streaming (word-by-word).
    Replace later with real token streaming.
    """

    words = text.split()

    for word in words:
        yield word + " "
        await asyncio.sleep(0.03)


# -----------------------------
# Non-Streaming Endpoint
# -----------------------------

@app.post("/chat")
async def chat(request: ChatRequest):

    try:

        session_id = get_session(request.session_id)

        logger.info(f"[CHAT] Session: {session_id}")
        logger.info(f"[USER] {request.message}")

        sessions[session_id].append({
            "role": "user",
            "content": request.message
        })

        # Run agent system
        response = run_dynamic_system(request.message)

        sessions[session_id].append({
            "role": "assistant",
            "content": response
        })

        logger.info(f"[ASSISTANT] {response[:100]}...")

        return {
            "session_id": session_id,
            "response": response
        }

    except Exception as e:

        logger.error("Error in /chat endpoint")
        logger.error(str(e))

        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


# -----------------------------
# Streaming Endpoint
# -----------------------------

@app.post("/chat-stream")
async def chat_stream(request: ChatRequest):

    try:

        session_id = get_session(request.session_id)

        logger.info(f"[STREAM] Session: {session_id}")
        logger.info(f"[USER] {request.message}")

        sessions[session_id].append({
            "role": "user",
            "content": request.message
        })

        # Run agent system (blocking for now)
        response_text = run_dynamic_system(request.message)

        sessions[session_id].append({
            "role": "assistant",
            "content": response_text
        })

        logger.info(f"[ASSISTANT STREAM READY]")

        return StreamingResponse(
            stream_response(response_text),
            media_type="text/plain"
        )

    except Exception as e:

        logger.error("Error in /chat-stream endpoint")
        logger.error(str(e))

        raise HTTPException(
            status_code=500,
            detail="Streaming error"
        )
    
@app.get("/metrics")
def metrics():
    return {
        "total_sessions": len(sessions),
        "status": "running"
    }