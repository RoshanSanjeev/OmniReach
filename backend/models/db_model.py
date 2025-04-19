from sqlalchemy import Column, String, Boolean, DateTime, Integer, Text
from sqlalchemy.orm import declarative_base
from backend.database import Base
from datetime import datetime

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    platform = Column(String)
    status = Column(String)
    budget = Column(Float)

class AccessLog(Base):
    __tablename__ = "access_logs"

    id = Column(Integer, primary_key=True, index=True)
    wallet = Column(String, index=True, nullable=False)
    collection = Column(String, index=True, nullable=False)
    access = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<AccessLog(wallet={self.wallet}, collection={self.collection}, access={self.access})>"

class PaymentLog(Base):
    __tablename__ = "payment_logs"

    id = Column(Integer, primary_key=True, index=True)
    wallet = Column(String, index=True, nullable=False)
    status = Column(String, default="pending")  # Options: pending, paid, failed
    payment_url = Column(Text, nullable=True)
    tx_id = Column(String, unique=True, nullable=True)  # Optional: track on-chain TX
    timestamp = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<PaymentLog(wallet={self.wallet}, status={self.status}, tx_id={self.tx_id})>"