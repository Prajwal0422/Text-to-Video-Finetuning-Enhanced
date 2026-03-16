"""
AI Retry Manager - Production-Ready Retry Engine
Handles API failures, timeouts, and rate limits with exponential backoff
"""

import time
import logging
from typing import Callable, Any, Optional, Dict
from functools import wraps

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RetryConfig:
    """Configuration for retry behavior"""
    MAX_RETRIES = 3
    BASE_DELAY = 5  # seconds
    MAX_DELAY = 20  # seconds
    EXPONENTIAL_BASE = 2
    
    # Error patterns to detect
    TRAFFIC_ERRORS = [
        "high traffic",
        "rate limit",
        "too many requests",
        "service unavailable",
        "503",
        "429",
        "queue full",
        "model busy"
    ]
    
    TIMEOUT_ERRORS = [
        "timeout",
        "timed out",
        "connection timeout",
        "read timeout"
    ]


class RetryManager:
    """
    Manages retry logic for AI model requests
    
    Features:
    - Exponential backoff (5s → 10s → 20s)
    - Traffic/queue error detection
    - Timeout error detection
    - Detailed logging
    """
    
    def __init__(self, config: Optional[RetryConfig] = None):
        self.config = config or RetryConfig()
        self.retry_count = 0
        self.total_wait_time = 0
    
    def calculate_delay(self, attempt: int) -> float:
        """
        Calculate exponential backoff delay
        
        Args:
            attempt: Current retry attempt (0-indexed)
        
        Returns:
            Delay in seconds (5s → 10s → 20s)
        """
        delay = self.config.BASE_DELAY * (self.config.EXPONENTIAL_BASE ** attempt)
        return min(delay, self.config.MAX_DELAY)
    
    def is_retryable_error(self, error: Exception) -> bool:
        """
        Check if error is retryable
        
        Args:
            error: Exception to check
        
        Returns:
            True if error should trigger retry
        """
        error_str = str(error).lower()
        
        # Check for traffic errors
        for pattern in self.config.TRAFFIC_ERRORS:
            if pattern in error_str:
                logger.warning(f"🚦 Traffic error detected: {pattern}")
                return True
        
        # Check for timeout errors
        for pattern in self.config.TIMEOUT_ERRORS:
            if pattern in error_str:
                logger.warning(f"⏱️  Timeout error detected: {pattern}")
                return True
        
        return False
    
    def retry_with_backoff(
        self,
        func: Callable,
        *args,
        on_retry: Optional[Callable[[int, float, Exception], None]] = None,
        **kwargs
    ) -> Any:
        """
        Execute function with retry logic
        
        Args:
            func: Function to execute
            *args: Function arguments
            on_retry: Optional callback(attempt, delay, error)
            **kwargs: Function keyword arguments
        
        Returns:
            Function result
        
        Raises:
            Last exception if all retries fail
        """
        last_exception = None
        
        for attempt in range(self.config.MAX_RETRIES + 1):
            try:
                logger.info(f"🔄 Attempt {attempt + 1}/{self.config.MAX_RETRIES + 1}")
                result = func(*args, **kwargs)
                
                if attempt > 0:
                    logger.info(f"✅ Success after {attempt} retries")
                
                return result
                
            except Exception as e:
                last_exception = e
                
                # Check if we should retry
                if attempt < self.config.MAX_RETRIES and self.is_retryable_error(e):
                    delay = self.calculate_delay(attempt)
                    self.retry_count += 1
                    self.total_wait_time += delay
                    
                    logger.warning(
                        f"❌ Attempt {attempt + 1} failed: {str(e)[:100]}"
                    )
                    logger.info(
                        f"⏳ Retrying in {delay}s... "
                        f"({self.config.MAX_RETRIES - attempt} retries left)"
                    )
                    
                    # Call retry callback if provided
                    if on_retry:
                        on_retry(attempt + 1, delay, e)
                    
                    time.sleep(delay)
                else:
                    # No more retries or non-retryable error
                    if attempt >= self.config.MAX_RETRIES:
                        logger.error(
                            f"💥 All {self.config.MAX_RETRIES} retries exhausted"
                        )
                    else:
                        logger.error(f"💥 Non-retryable error: {str(e)[:100]}")
                    
                    raise last_exception
        
        # Should never reach here, but just in case
        raise last_exception
    
    def get_stats(self) -> Dict[str, Any]:
        """Get retry statistics"""
        return {
            'total_retries': self.retry_count,
            'total_wait_time': self.total_wait_time,
            'max_retries': self.config.MAX_RETRIES
        }


def with_retry(max_retries: int = 3):
    """
    Decorator for automatic retry logic
    
    Usage:
        @with_retry(max_retries=3)
        def call_ai_model(prompt):
            return model.generate(prompt)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            manager = RetryManager()
            config = RetryConfig()
            config.MAX_RETRIES = max_retries
            manager.config = config
            
            return manager.retry_with_backoff(func, *args, **kwargs)
        
        return wrapper
    return decorator


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("AI RETRY MANAGER - TEST")
    print("=" * 60)
    
    # Simulate API call that fails twice then succeeds
    attempt_count = 0
    
    def flaky_api_call(prompt: str) -> str:
        global attempt_count
        attempt_count += 1
        
        if attempt_count <= 2:
            raise Exception("Model experiencing high traffic. Please retry.")
        
        return f"Generated video for: {prompt}"
    
    # Test retry logic
    manager = RetryManager()
    
    try:
        result = manager.retry_with_backoff(
            flaky_api_call,
            "A beautiful sunset"
        )
        print(f"\n✅ Result: {result}")
        print(f"\n📊 Stats: {manager.get_stats()}")
    except Exception as e:
        print(f"\n❌ Failed: {e}")
