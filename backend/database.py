from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# 🔄 Load environment variables from .env if present
load_dotenv()

# 📦 Get DB connection URL (default to local if not provided)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:omni@localhost:5432/omnireach"
)

# 🔗 Create the engine
engine = create_engine(DATABASE_URL)

# 🧪 Session factory (used via dependency injection)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 🧱 Declarative Base class for models
Base = declarative_base()

# 📥 DB session dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()