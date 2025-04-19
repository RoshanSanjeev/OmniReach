from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from crew_definition import ResearchCrew

router = APIRouter(prefix="/api/research", tags=["Research"])

class ResearchQuery(BaseModel):
    query: str

@router.post("/")
async def run_research(query: ResearchQuery):
    try:
        crew = ResearchCrew(verbose=True)
        result = crew.crew.kickoff(inputs={"text": query.query})
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))