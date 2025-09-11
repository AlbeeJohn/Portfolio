from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import time
import logging

logger = logging.getLogger(__name__)

class SecurityMiddleware(BaseHTTPMiddleware):
    """Add security headers and request logging"""
    
    def __init__(self, app, enable_logging: bool = True):
        super().__init__(app)
        self.enable_logging = enable_logging
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Log request if enabled
        if self.enable_logging:
            logger.info(f"Request: {request.method} {request.url.path}")
        
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        response.headers["X-Robots-Tag"] = "index, follow"
        
        # Add performance headers
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(round(process_time * 1000, 2))
        
        # Log response if enabled
        if self.enable_logging:
            logger.info(
                f"Response: {response.status_code} "
                f"({round(process_time * 1000, 2)}ms)"
            )
        
        return response

class CompressionMiddleware(BaseHTTPMiddleware):
    """Simple compression middleware"""
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Add compression hint
        if "gzip" in request.headers.get("accept-encoding", "").lower():
            response.headers["Content-Encoding"] = "gzip"
        
        return response