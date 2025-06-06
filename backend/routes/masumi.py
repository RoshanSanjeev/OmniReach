from fastapi import APIRouter, Request
from backend.services.masumi_transaction import (
    verify_nft_ownership,
    check_payment_status,
    initiate_payment
)
from backend.models.payment_model import (
    VerifyAccessResponse,
    PaymentStatusResponse,
    InitiatePaymentResponse
)

router = APIRouter(prefix="/api/masumi", tags=["Masumi"])

@router.post("/verify-access", response_model=VerifyAccessResponse)
async def verify_access(req: Request):
    """
    Verifies whether the given wallet owns the required NFT.
    """
    data = await req.json()
    wallet = data.get("wallet")
    collection = data.get("collection")
    return await verify_nft_ownership(wallet, collection)

@router.post("/payment-status", response_model=PaymentStatusResponse)
async def payment_status(req: Request):
    """
    Checks if the wallet has successfully completed the payment.
    """
    data = await req.json()
    wallet = data.get("wallet")
    return await check_payment_status(wallet)

@router.post("/pay-to-unlock", response_model=InitiatePaymentResponse)
async def pay_to_unlock(req: Request):
    """
    Initiates a payment or minting process for the given wallet.
    """
    data = await req.json()
    wallet = data.get("wallet")
    return await initiate_payment(wallet)