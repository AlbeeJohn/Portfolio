from fastapi import APIRouter, HTTPException, Depends, Request
from models.portfolio import Portfolio, ContactMessage, ContactMessageCreate
from datetime import datetime
from middleware.cache import cached_response
from middleware.rate_limiting import rate_limit, contact_limiter
from config.database import get_db
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/portfolio")
@cached_response(ttl=1800)  # Cache for 30 minutes
@rate_limit()
async def get_portfolio(request: Request, db = Depends(get_db)):
    """Get complete portfolio data with caching"""
    try:
        portfolio = await db.portfolio.find_one({}, {"_id": 0})
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        logger.info("Portfolio data retrieved successfully")
        return portfolio
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving portfolio: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/portfolio")
async def update_portfolio(portfolio_data: Portfolio, db = Depends(get_db)):
    """Update portfolio data"""
    try:
        portfolio_dict = portfolio_data.dict()
        portfolio_dict["updated_at"] = datetime.utcnow()
        
        result = await db.portfolio.replace_one(
            {},
            portfolio_dict,
            upsert=True
        )
        
        if result.modified_count == 0 and result.upserted_id is None:
            raise HTTPException(status_code=400, detail="Failed to update portfolio")
        
        return {"message": "Portfolio updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/contact")
@rate_limit(limiter=contact_limiter)  # Stricter rate limit for contact form
async def create_contact_message(message_data: ContactMessageCreate, request: Request, db = Depends(get_db)):
    """Create a new contact message with rate limiting"""
    try:
        message = ContactMessage(**message_data.dict())
        message_dict = message.dict()
        
        result = await db.contact_messages.insert_one(message_dict)
        
        if not result.inserted_id:
            raise HTTPException(status_code=400, detail="Failed to save message")
        
        logger.info(f"New contact message created: {message.id}")
        return {
            "message": "Message sent successfully",
            "id": message.id
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating contact message: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/contact/messages")
async def get_contact_messages(db = Depends(get_db)):
    """Get all contact messages (admin endpoint)"""
    try:
        messages = await db.contact_messages.find({}, {"_id": 0}).sort("created_at", -1).to_list(100)
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/contact/messages/{message_id}/read")
async def mark_message_read(message_id: str, db = Depends(get_db)):
    """Mark a contact message as read"""
    try:
        result = await db.contact_messages.update_one(
            {"id": message_id},
            {"$set": {"read": True}}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Message not found")
        
        return {"message": "Message marked as read"}
    except HTTPException:
        raise  # Re-raise HTTPException without modification
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))