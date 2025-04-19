# backend/utils/logger.py

from datetime import datetime

def log_payment_attempt(wallet: str) -> dict:
    """
    Logs the time and wallet address for a payment attempt.
    """
    timestamp = datetime.utcnow().isoformat()
    log = {
        "wallet": wallet,
        "timestamp": timestamp,
        "status": "pending",
        "message": "Payment attempt logged."
    }
    print(f"[MASUMI] Payment log for {wallet} at {timestamp}")
    return log