import uuid
from datetime import datetime

def generate_payment_url(wallet: str) -> str:
    tx_id = uuid.uuid4()
    return f"https://masumi.io/pay/{wallet}?tx={tx_id}"

def log_payment_attempt(wallet: str):
    timestamp = datetime.utcnow().isoformat()
    return {
        "wallet": wallet,
        "timestamp": timestamp,
        "status": "pending",
        "message": "Payment attempt logged."
    }
