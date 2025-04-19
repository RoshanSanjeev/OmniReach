import requests
import os

MASUMI_API_KEY = os.getenv("MASUMI_API_KEY")
MASUMI_VERIFY_URL = "https://api.masumi.io/v1/verify"  # Update if needed

def verify_nft_access(wallet: str, collection: str) -> dict:
    """
    Verifies if the given wallet owns the required NFT by calling Masumi API.
    
    Args:
        wallet (str): Wallet address of the user.
        collection (str): NFT collection slug.

    Returns:
        dict: {
            "valid": bool,
            "wallet": str,
            "collection": str,
            "timestamp": str (optional),
            "error": str (if failed)
        }
    """
    headers = {
        "Authorization": f"Bearer {MASUMI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "wallet": wallet,
        "collection": collection
    }

    try:
        response = requests.post(MASUMI_VERIFY_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"[Masumi API HTTP error] {http_err}")
        return {"valid": False, "wallet": wallet, "collection": collection, "error": str(http_err)}
    except Exception as err:
        print(f"[Masumi API general error] {err}")
        return {"valid": False, "wallet": wallet, "collection": collection, "error": str(err)}