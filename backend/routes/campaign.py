from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.db_model import Campaign  # 모델 정의가 db_model.py 안에 있다고 가정
from pydantic import BaseModel
import uuid

router = APIRouter(prefix="/api/campaign", tags=["Campaign"])

# Pydantic 모델
class CampaignCreate(BaseModel):
    name: str
    platform: str
    status: str
    budget: float

class CampaignOut(CampaignCreate):
    id: str

# 캠페인 생성
@router.post("/", response_model=CampaignOut)
def create_campaign(data: CampaignCreate, db: Session = Depends(get_db)):
    new_campaign = Campaign(
        id=str(uuid.uuid4()),
        name=data.name,
        platform=data.platform,
        status=data.status,
        budget=data.budget
    )
    db.add(new_campaign)
    db.commit()
    db.refresh(new_campaign)
    return new_campaign

# 캠페인 전체 조회
@router.get("/", response_model=list[CampaignOut])
def list_campaigns(db: Session = Depends(get_db)):
    return db.query(Campaign).all()