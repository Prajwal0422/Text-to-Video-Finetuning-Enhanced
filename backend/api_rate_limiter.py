"""
Advanced API Rate Limiter
Prevents API abuse and manages request quotas
"""

import time
from typing import Dict, Optional
from collections import deque
from datetime import datetime, timedelta
import threading

class APIRateLimiter:
    def __init__(self):
        self.limits = {
            'per_minute': 10,
            'per_hour': 100,
            'per_day': 1000
        }
        
        self.requests = {
            'minute': deque(),
            'hour': deque(),
            'day': deque()
        }
        
        self.lock = threading.Lock()
        self.blocked_ips = {}
    
    def check_limit(self, identifier: str = "default") -> Dict:
        """Check if request is allowed"""
        with self.lock:
            now = time.time()
            
            # Clean old requests
            self._clean_old_requests(now)
            
            # Check if blocked
            if identifier in self.blocked_ips:
                block_until = self.blocked_ips[identifier]
                if now < block_until:
                    remaining = int(block_until - now)
                    return {
                        'allowed': False,
                        'reason': 'blocked',
                        'retry_after': remaining
                    }
                else:
                    del self.blocked_ips[identifier]
            
            # Check limits
            minute_count = len(self.requests['minute'])
            hour_count = len(self.requests['hour'])
            day_count = len(self.requests['day'])
            
            # Check each limit
            if minute_count >= self.limits['per_minute']:
                return {
                    'allowed': False,
                    'reason': 'rate_limit_minute',
                    'limit': self.limits['per_minute'],
                    'current': minute_count,
                    'retry_after': 60
                }
            
            if hour_count >= self.limits['per_hour']:
                return {
                    'allowed': False,
                    'reason': 'rate_limit_hour',
                    'limit': self.limits['per_hour'],
                    'current': hour_count,
                    'retry_after': 3600
                }
            
            if day_count >= self.limits['per_day']:
                return {
                    'allowed': False,
                    'reason': 'rate_limit_day',
                    'limit': self.limits['per_day'],
                    'current': day_count,
                    'retry_after': 86400
                }
            
            # Record request
            self.requests['minute'].append(now)
            self.requests['hour'].append(now)
            self.requests['day'].append(now)
            
            return {
                'allowed': True,
                'remaining': {
                    'minute': self.limits['per_minute'] - minute_count - 1,
                    'hour': self.limits['per_hour'] - hour_count - 1,
                    'day': self.limits['per_day'] - day_count - 1
                }
            }
    
    def _clean_old_requests(self, now: float):
        """Remove old requests outside time windows"""
        # Clean minute window (60 seconds)
        while self.requests['minute'] and now - self.requests['minute'][0] > 60:
            self.requests['minute'].popleft()
        
        # Clean hour window (3600 seconds)
        while self.requests['hour'] and now - self.requests['hour'][0] > 3600:
            self.requests['hour'].popleft()
        
        # Clean day window (86400 seconds)
        while self.requests['day'] and now - self.requests['day'][0] > 86400:
            self.requests['day'].popleft()
    
    def block_identifier(self, identifier: str, duration: int = 3600):
        """Block an identifier for specified duration (seconds)"""
        with self.lock:
            block_until = time.time() + duration
            self.blocked_ips[identifier] = block_until
            print(f"🚫 Blocked {identifier} for {duration}s")
    
    def unblock_identifier(self, identifier: str):
        """Unblock an identifier"""
        with self.lock:
            if identifier in self.blocked_ips:
                del self.blocked_ips[identifier]
                print(f"✅ Unblocked {identifier}")
    
    def get_stats(self) -> Dict:
        """Get current rate limiter statistics"""
        with self.lock:
            now = time.time()
            self._clean_old_requests(now)
            
            return {
                'requests_last_minute': len(self.requests['minute']),
                'requests_last_hour': len(self.requests['hour']),
                'requests_last_day': len(self.requests['day']),
                'limits': self.limits,
                'blocked_count': len(self.blocked_ips)
            }
    
    def reset_limits(self):
        """Reset all limits"""
        with self.lock:
            self.requests = {
                'minute': deque(),
                'hour': deque(),
                'day': deque()
            }
            self.blocked_ips.clear()
            print("✅ Rate limits reset")
    
    def update_limits(self, per_minute: Optional[int] = None,
                     per_hour: Optional[int] = None,
                     per_day: Optional[int] = None):
        """Update rate limits"""
        with self.lock:
            if per_minute is not None:
                self.limits['per_minute'] = per_minute
            if per_hour is not None:
                self.limits['per_hour'] = per_hour
            if per_day is not None:
                self.limits['per_day'] = per_day
            
            print(f"✅ Limits updated: {self.limits}")


# Global instance
rate_limiter = APIRateLimiter()


if __name__ == "__main__":
    print("API Rate Limiter Test")
    print("=" * 60)
    
    # Test rate limiting
    print("\nTesting rate limits...")
    
    for i in range(12):
        result = rate_limiter.check_limit("test_user")
        
        if result['allowed']:
            print(f"Request {i+1}: ✅ Allowed (remaining: {result['remaining']['minute']}/min)")
        else:
            print(f"Request {i+1}: ❌ Blocked ({result['reason']})")
            break
    
    # Show stats
    print("\nCurrent Stats:")
    stats = rate_limiter.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
