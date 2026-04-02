import uuid
import asyncio
import logging
import time
from utils.evaluator import evaluate_response
from utils.logger import log_request, log_response, log_error
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
        start_time = time.time()

        # -----------------------------
        # Session Handling
        # -----------------------------
        session_id = get_session(request.session_id)
        evaluation = evaluate_response(request.message, response)
        
        # -----------------------------
        # Log Incoming Request
        # -----------------------------
        log_request(session_id, request.message)

        # Store user message
        sessions[session_id].append({
            "role": "user",
            "content": request.message
        })

        # -----------------------------
        # Run Agent System
        # -----------------------------
        response = run_dynamic_system(request.message)

        # -----------------------------
        # Store Response
        # -----------------------------
        sessions[session_id].append({
            "role": "assistant",
            "content": response
        })

        # -----------------------------
        # Latency Tracking
        # -----------------------------
        latency = time.time() - start_time

        # -----------------------------
        # Logging
        # -----------------------------
        log_response(session_id, response)
        logger.info(f"[LATENCY] Session: {session_id} | {latency:.2f}s")

        # -----------------------------
        # Final Response
        # -----------------------------
        return {
            "session_id": session_id,
            "response": response,
            "latency_seconds": round(latency, 2)
        }

    except Exception as e:

        # -----------------------------
        # Error Logging
        # -----------------------------
        log_error(e)

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