import uuid
import asyncio
import logging
import time
from fastapi import Header
from utils.security import check_rate_limit, verify_api_key
from utils.cache import get_cache, set_cache
from utils.evaluator import evaluate_response
from utils.logger import log_request, log_response, log_error, log_evaluation
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
async def chat(request: ChatRequest, x_api_key: str = Header(None)):

    try:
        start_time = time.time()
        
        # -----------------------------
        # 0. Security Layer (FIRST)
        # -----------------------------

        if not verify_api_key(x_api_key):
            raise HTTPException(status_code=401, detail="Invalid API Key")

        client_id = x_api_key  # can also use IP later

        if not check_rate_limit(client_id):
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Try again later."
            )

        # -----------------------------
        # 1. Session Handling (MUST FIRST)
        # -----------------------------
        session_id = get_session(request.session_id)

        # Safety check (extra protection)
        if session_id not in sessions:
            sessions[session_id] = []

        # -----------------------------
        # 2. Log Request
        # -----------------------------
        log_request(session_id, request.message)

        # Store user message
        sessions[session_id].append({
            "role": "user",
            "content": request.message
        })

        # -----------------------------
        # 3. Run Agent System
        # -----------------------------
        response = run_dynamic_system(request.message)

        # -----------------------------
        # 4. Evaluate Response
        # -----------------------------
        evaluation = evaluate_response(request.message, response)

        # -----------------------------
        # 5. Store Assistant Response
        # -----------------------------
        sessions[session_id].append({
            "role": "assistant",
            "content": response
        })

        # -----------------------------
        # 6. Latency Tracking
        # -----------------------------
        latency = time.time() - start_time

        # -----------------------------
        # 7. Logging (ALL AFTER EXECUTION)
        # -----------------------------
        log_response(session_id, response)
        log_evaluation(session_id, evaluation)

        logger.info(
            f"[LATENCY] Session: {session_id} | {latency:.2f}s"
        )

        cache_key = request.message.lower().strip()

        cached_response = get_cache(cache_key)
        

        set_cache(cache_key, response)

        if cached_response:
            logger.info(f"[CACHE HIT] {cache_key}")

            return {
                "session_id": session_id,
                "response": cached_response,
                "cached": True
            }

    except Exception as e:

        # -----------------------------
        # Error Handling
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