from pydantic import BaseModel
from typing import Optional

class VerifyAccessResponse(BaseModel):
    access: bool
    message: str

class PaymentStatusResponse(BaseModel):
    wallet: str
    paid: bool
    message: Optional[str] = None

class InitiatePaymentResponse(BaseModel):
    wallet: str
    status: str
    payment_url: Optional[str] = None
    message: Optional[str] = None