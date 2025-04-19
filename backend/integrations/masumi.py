import requests
import os

MASUMI_API_KEY = os.getenv("MASUMI_API_KEY")

def verify_nft_access(wallet: str, collection: str):
    url = "https://api.masumi.io/v1/verify"
    headers = {
        "Authorization": f"Bearer {MASUMI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "wallet": wallet,
        "collection": collection
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()
