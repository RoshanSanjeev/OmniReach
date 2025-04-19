from sqlalchemy import Column, String, DateTime, Boolean, Float
from backend.database import Base
from datetime import datetime

class Event(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True, index=True)
    campaign_id = Column(String)
    video_id = Column(String, nullable=True)
    persona_id = Column(String, nullable=True)
    event_type = Column(String)  # e.g. click, conversion
    created_at = Column(DateTime, default=datetime.utcnow)
    sent_to_ga = Column(Boolean, default=False)