from fastapi import HTTPException, Request
from functools import wraps
import time
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class RateLimiter:
    """Simple in-memory rate limiter"""
    
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = {}
    
    def _get_client_id(self, request: Request) -> str:
        """Get client identifier"""
        # Try to get real IP from headers (for production behind proxy)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        return request.client.host if request.client else "unknown"
    
    def is_allowed(self, request: Request) -> Tuple[bool, int]:
        """Check if request is allowed"""
        client_id = self._get_client_id(request)
        current_time = time.time()
        
        # Clean old requests (older than 1 minute)
        if client_id in self.requests:
            self.requests[client_id] = [
                req_time for req_time in self.requests[client_id]
                if current_time - req_time < 60
            ]
        else:
            self.requests[client_id] = []
        
        # Check if limit exceeded
        if len(self.requests[client_id]) >= self.requests_per_minute:
            oldest_request = min(self.requests[client_id])
            reset_time = int(oldest_request + 60 - current_time)
            logger.warning(f"Rate limit exceeded for {client_id}")
            return False, reset_time
        
        # Add current request
        self.requests[client_id].append(current_time)
        return True, 0

# Global rate limiter instances
general_limiter = RateLimiter(requests_per_minute=100)  # General API
contact_limiter = RateLimiter(requests_per_minute=5)    # Contact form

def rate_limit(limiter: RateLimiter = general_limiter):
    """Rate limiting decorator"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Find request object in args
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            
            if request:
                allowed, reset_time = limiter.is_allowed(request)
                if not allowed:
                    raise HTTPException(
                        status_code=429,
                        detail="Rate limit exceeded",
                        headers={"Retry-After": str(reset_time)}
                    )
            
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator