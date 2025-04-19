from crewai import Agent
from backend.services.masumi_transaction import (
    verify_nft_ownership,
    check_payment_status,
    initiate_payment
)

# 🧠 CrewAI Agent definition (optional for crew composition)
masumi_agent = Agent(
    name="MasumiVerifier",
    role="Verifies NFT ownership and payment status",
    goal="Ensure only eligible users can unlock access to protected features",
    backstory="This agent acts as a gatekeeper by verifying whether a wallet has the required NFT and has completed payment before allowing access to gated functionality.",
    verbose=True
)

# ✅ Core agent flow function
# This can be used in FastAPI directly or in CrewAI task
async def run_agent_flow(wallet: str, collection: str):
    """
    Executes the access verification logic:
    1. Check NFT ownership
    2. Check payment status
    3. Return access response accordingly
    """

    # Step 1: Verify NFT ownership via Blockfrost or Masumi
    access = await verify_nft_ownership(wallet, collection)
    if not access["has_access"]:
        return {
            "wallet": wallet,
            "access": False,
            "reason": "NFT not owned"
        }

    # Step 2: Check payment status
    payment = await check_payment_status(wallet)
    if payment.get("status") != "paid":
        tx = await initiate_payment(wallet)
        return {
            "wallet": wallet,
            "access": False,
            "reason": "Payment not completed",
            "next_step": "pay-to-unlock",
            "tx_link": tx["tx_link"]
        }

    # Step 3: All conditions met
    return {
        "wallet": wallet,
        "access": True,
        "status": "ready",
        "message": "NFT owned and payment confirmed"
    }