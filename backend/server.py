from fastapi import FastAPI, APIRouter, Depends
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List
import uuid
from datetime import datetime
from routes.portfolio import router as portfolio_router
from routes.health import router as health_router
from middleware.security import SecurityMiddleware
from config.database import db_manager, get_db

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Enhanced logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('/tmp/portfolio_api.log')
    ]
)
logger = logging.getLogger(__name__)

# Create the main app with enhanced metadata
app = FastAPI(
    title="Albee John Portfolio API",
    description="High-performance API for Data Science Portfolio",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Add performance and security middlewares
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(SecurityMiddleware, enable_logging=True)

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Define Models for backward compatibility
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "Albee John Portfolio API - Data Analyst & Science Enthusiast"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate, db = Depends(get_db)):
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    _ = await db.status_checks.insert_one(status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks(db = Depends(get_db)):
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]

# Include portfolio routes
api_router.include_router(portfolio_router)

# Include health routes
api_router.include_router(health_router)

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Application startup and shutdown events
@app.on_event("startup")
async def startup_db_client():
    """Initialize database connection on startup"""
    try:
        await db_manager.connect()
        logger.info("✅ Application startup completed successfully")
    except Exception as e:
        logger.error(f"❌ Application startup failed: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_db_client():
    """Close database connection on shutdown"""
    try:
        await db_manager.disconnect()
        logger.info("✅ Application shutdown completed successfully")
    except Exception as e:
        logger.error(f"❌ Application shutdown failed: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
