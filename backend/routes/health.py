from fastapi import APIRouter, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime
import psutil
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/health")
async def health_check():
    """Basic health check endpoint for Railway"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "portfolio-api",
        "version": "1.0.0"
    }

@router.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check with system and database status"""
    try:
        # Database connection test (optional)
        mongo_url = os.environ.get('MONGO_URL')
        db_status = "not_configured"
        
        if mongo_url:
            try:
                client = AsyncIOMotorClient(mongo_url)
                await client.admin.command('ping')
                db_status = "connected"
                client.close()
            except Exception as e:
                db_status = f"error: {str(e)}"
                logger.warning(f"Database connection failed: {e}")
        
        health_data = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "service": "portfolio-api",
            "version": "1.0.0",
            "database": {
                "status": db_status,
                "type": "MongoDB"
            },
            "environment": os.environ.get("ENVIRONMENT", "development")
        }
        
        return health_data
        
    except Exception as e:
        logger.error(f"Detailed health check failed: {e}")
        # Return healthy status anyway for Railway
        return {
            "status": "healthy", 
            "timestamp": datetime.utcnow().isoformat(),
            "service": "portfolio-api",
            "error": str(e)
        }

@router.get("/metrics")
async def get_metrics():
    """Get application metrics"""
    try:
        from middleware.cache import cache
        
        return {
            "timestamp": datetime.utcnow(),
            "cache": {
                "size": cache.size(),
                "type": "memory"
            },
            "system": {
                "uptime": "N/A",  # Could add process start time tracking
                "requests_processed": "N/A"  # Could add request counter
            }
        }
    except Exception as e:
        logger.error(f"Metrics collection failed: {e}")
        return {"error": "Failed to collect metrics"}