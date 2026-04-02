import logging
import os

# Create logs directory
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)



def log_request(session_id, message):
    logger.info(f"[REQUEST] Session: {session_id} | Message: {message}")


def log_response(session_id, response):
    logger.info(f"[RESPONSE] Session: {session_id} | Response: {response[:200]}")


def log_error(error):
    logger.error(f"[ERROR] {str(error)}")

def log_evaluation(session_id, evaluation):
    logger.info(f"[EVALUATION] Session: {session_id} | {evaluation}")