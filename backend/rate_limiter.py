"""
Rate Limiter for API Protection
Prevents abuse and manages request throttling
"""

import time
from typing import Dict, Optional
from collections import defaultdict

class RateLimiter:
    """Simple rate limiter using token bucket algorithm"""
    
    def __init__(self, max_requests: int = 10, window_seconds: int = 60):
        """
        Initialize rate limiter
        
        Args:
            max_requests: Maximum requests allowed in window
            window_seconds: Time window in seconds
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, list] = defaultdict(list)
    
    def is_allowed(self, client_id: str) -> bool:
        """
        Check if request is allowed for client
        
        Args:
            client_id: Unique client identifier (IP, user ID, etc.)
        
        Returns:
            True if request is allowed, False if rate limited
        """
        now = time.time()
        
        # Clean old requests outside window
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if now - req_time < self.window_seconds
        ]
        
        # Check if under limit
        if len(self.requests[client_id]) < self.max_requests:
            self.requests[client_id].append(now)
            return True
        
        return False
    
    def get_remaining(self, client_id: str) -> int:
        """Get remaining requests for client"""
        now = time.time()
        
        # Clean old requests
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if now - req_time < self.window_seconds
        ]
        
        return max(0, self.max_requests - len(self.requests[client_id]))
    
    def get_reset_time(self, client_id: str) -> Optional[float]:
        """Get time until rate limit resets"""
        if not self.requests[client_id]:
            return None
        
        oldest_request = min(self.requests[client_id])
        reset_time = oldest_request + self.window_seconds
        
        return max(0, reset_time - time.time())
