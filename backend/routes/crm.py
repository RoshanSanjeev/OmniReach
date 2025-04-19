from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.event_model import Event
from sqlalchemy import func

router = APIRouter(prefix="/api/crm", tags=["CRM"])

@router.get("/events")
def get_event_feed(db: Session = Depends(get_db)):
    return db.query(Event).order_by(Event.created_at.desc()).limit(100).all()

@router.get("/summary")
def get_campaign_stats(db: Session = Depends(get_db)):
    return {
        "clicks": db.query(Event).filter_by(event_type="click").count(),
        "conversions": db.query(Event).filter_by(event_type="conversion").count()
    }