import httpx
import os

BLOCKFROST_API_KEY = os.getenv("BLOCKFROST_KEY")
BASE_URL = "https://cardano-mainnet.blockfrost.io/api/v0"

async def check_nft_ownership(wallet_address: str, policy_id: str) -> bool:
    headers = {"project_id": BLOCKFROST_API_KEY}
    assets_url = f"{BASE_URL}/addresses/{wallet_address}/assets"

    async with httpx.AsyncClient() as client:
        res = await client.get(assets_url, headers=headers)
        if res.status_code != 200:
            return False
        assets = res.json()
        return any(asset["unit"].startswith(policy_id) for asset in assets)