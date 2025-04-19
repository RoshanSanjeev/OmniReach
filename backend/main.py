from fastapi import FastAPI
from .routes import masumi

app = FastAPI()
app.include_router(masumi.router)