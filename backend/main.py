from fastapi import FastAPI
from .routes import masumi
from backend.routes import masumi, agent, campaign, crm, tracking
from backend.routes import research 

app = FastAPI()
app.include_router(masumi.router)
app.include_router(agent.router)
app.include_router(campaign.router)
app.include_router(crm.router)
app.include_router(tracking.router)
app.include_router(research.router) 