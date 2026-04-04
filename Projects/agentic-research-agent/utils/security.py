import time

# Store request timestamps per user
rate_limit_store = {}

# Config
MAX_REQUESTS = 5
TIME_WINDOW = 60  # seconds


def check_rate_limit(client_id):

    now = time.time()

    requests = rate_limit_store.get(client_id, [])

    # Remove old requests
    requests = [r for r in requests if now - r < TIME_WINDOW]

    if len(requests) >= MAX_REQUESTS:
        return False

    requests.append(now)
    rate_limit_store[client_id] = requests

    return True