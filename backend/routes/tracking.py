from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.event_model import Event
import uuid
import datetime

router = APIRouter(prefix="/api/tracking", tags=["Tracking"])

@router.post("/click")
async def log_click(req: Request, db: Session = Depends(get_db)):
    data = await req.json()

    new_event = Event(
        id=str(uuid.uuid4()),
        campaign_id=data.get("campaign_id"),
        video_id=data.get("video_id"),
        persona_id=data.get("persona_id"),
        event_type="click",
        created_at=datetime.datetime.utcnow(),
        sent_to_ga=False
    )
    db.add(new_event)
    db.commit()
    return {"status": "click logged", "event_id": new_event.id}