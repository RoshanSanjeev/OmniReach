from fastapi import APIRouter, Request
from backend.agents.masumi_agent import run_agent_flow
from backend.crew_masumi import MasumiCrew

router = APIRouter(prefix="/api/agent", tags=["Agent"])

@router.post("/verify-access")
async def verify_access_agent(req: Request):
    """
    Executes direct agent function to check NFT + payment access.
    """
    data = await req.json()
    wallet = data.get("wallet")
    collection = data.get("collection")

    if not wallet or not collection:
        return {"error": "wallet and collection are required"}

    result = await run_agent_flow(wallet=wallet, collection=collection)
    return result


# CrewAI version using MasumiCrew class
masumi_crew = MasumiCrew()

@router.post("/verify-access-crew")
async def verify_agent_with_crew(req: Request):
    """
    Executes the same access logic using CrewAI crew.run()
    """
    data = await req.json()
    return masumi_crew.crew.kickoff(inputs=data)