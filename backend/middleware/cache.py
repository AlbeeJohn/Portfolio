from fastapi import Request, Response
from functools import wraps
import json
import hashlib
from typing import Dict, Any, Optional
import time
import logging

logger = logging.getLogger(__name__)

class MemoryCache:
    """Simple in-memory cache for API responses"""
    
    def __init__(self, default_ttl: int = 3600):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.default_ttl = default_ttl
        
    def _generate_key(self, request: Request) -> str:
        """Generate cache key from request"""
        key_data = f"{request.method}:{request.url.path}:{request.url.query}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """Get cached value"""
        if key in self.cache:
            cache_entry = self.cache[key]
            if time.time() < cache_entry['expires_at']:
                logger.info(f"Cache HIT for key: {key[:8]}...")
                return cache_entry['data']
            else:
                # Cache expired, remove it
                del self.cache[key]
                logger.info(f"Cache EXPIRED for key: {key[:8]}...")
        
        logger.info(f"Cache MISS for key: {key[:8]}...")
        return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set cache value"""
        ttl = ttl or self.default_ttl
        expires_at = time.time() + ttl
        
        self.cache[key] = {
            'data': value,
            'expires_at': expires_at
        }
        
        logger.info(f"Cache SET for key: {key[:8]}... (TTL: {ttl}s)")
    
    def clear(self) -> None:
        """Clear all cache"""
        self.cache.clear()
        logger.info("Cache cleared")
    
    def size(self) -> int:
        """Get cache size"""
        return len(self.cache)

# Global cache instance
cache = MemoryCache(default_ttl=1800)  # 30 minutes default

def cached_response(ttl: int = 1800):
    """Decorator for caching API responses"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Find request object in args
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            
            if not request:
                # No request found, execute without caching
                return await func(*args, **kwargs)
            
            cache_key = cache._generate_key(request)
            
            # Try to get from cache first
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            
            # Only cache successful responses
            if result is not None:
                cache.set(cache_key, result, ttl)
            
            return result
        
        return wrapper
    return decorator