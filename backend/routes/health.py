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
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "service": "portfolio-api"
    }

@router.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check with system and database status"""
    try:
        # System metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Database connection test
        mongo_url = os.environ.get('MONGO_URL')
        db_status = "unknown"
        
        if mongo_url:
            try:
                client = AsyncIOMotorClient(mongo_url)
                await client.admin.command('ping')
                db_status = "connected"
                client.close()
            except Exception as e:
                db_status = f"error: {str(e)}"
                logger.error(f"Database health check failed: {e}")
        
        health_data = {
            "status": "healthy",
            "timestamp": datetime.utcnow(),
            "service": "portfolio-api",
            "version": "1.0.0",
            "system": {
                "cpu_percent": cpu_percent,
                "memory": {
                    "total": round(memory.total / (1024**3), 2),  # GB
                    "used": round(memory.used / (1024**3), 2),   # GB
                    "percent": memory.percent
                },
                "disk": {
                    "total": round(disk.total / (1024**3), 2),   # GB
                    "used": round(disk.used / (1024**3), 2),    # GB
                    "free": round(disk.free / (1024**3), 2),    # GB
                    "percent": round((disk.used / disk.total) * 100, 1)
                }
            },
            "database": {
                "status": db_status,
                "type": "MongoDB"
            }
        }
        
        # Determine overall status
        if db_status.startswith("error"):
            health_data["status"] = "degraded"
        elif cpu_percent > 90 or memory.percent > 90:
            health_data["status"] = "degraded"
        
        return health_data
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")

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