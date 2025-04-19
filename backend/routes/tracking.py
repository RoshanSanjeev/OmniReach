from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas import Event
import uuid
import datetime

router = APIRouter(prefix="/api/tracking", tags=["Tracking"])

@router.post("/click")
def log_click(request: Request, db: Session = Depends(get_db)):
    body = request.query_params
    new_event = Event(
        id=str(uuid.uuid4()),
        campaign_id=body.get("campaign_id"),
        video_id=body.get("video_id"),
        persona_id=body.get("persona_id"),
        event_type="click",
        created_at=datetime.datetime.utcnow(),
        sent_to_ga=False
    )
    db.add(new_event)
    db.commit()
    return {"status": "click logged"}