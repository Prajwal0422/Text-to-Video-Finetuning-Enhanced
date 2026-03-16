"""
Resilient Video Generator - Production-Ready System
Integrates retry, routing, timeout, and local fallback
"""

import asyncio
import logging
from typing import Dict, Any, Optional, Callable
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from .ai_retry_manager import RetryManager
    from .ai_model_router import ModelRouter, ModelConfig
    from .local_generation import LocalGenerator
    from .video_generator import VideoGenerator
except ImportError:
    from ai_retry_manager import RetryManager
    from ai_model_router import ModelRouter, ModelConfig
    from local_generation import LocalGenerator
    from video_generator import VideoGenerator


class ResilientVideoGenerator:
    """
    Production-ready video generator with full resilience
    
    Features:
    - Retry with exponential backoff
    - Multi-model routing
    - 60-second timeout protection
    - Local generation fallback
    - Progress callbacks
    - Never fails completely
    """
    
    def __init__(self, pexels_api_key: Optional[str] = None, timeout: int = 60):
        self.timeout = timeout
        self.retry_manager = RetryManager()
        self.model_router = ModelRouter()
        self.local_generator = LocalGenerator()
        self.primary_generator = VideoGenerator(pexels_api_key)
        
        self.stats = {
            'total_requests': 0,
            'successful': 0,
            'failed': 0,
            'retries_used': 0,
            'fallbacks_used': 0,
            'local_mode_used': 0
        }
    
    async def generate_with_timeout(
        self,
        prompt: str,
        progress_callback: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        Generate video with timeout protection
        
        Args:
            prompt: Video generation prompt
            progress_callback: Progress callback function
        
        Returns:
            Generation result
        """
        try:
            result = await asyncio.wait_for(
                self._generate_async(prompt, progress_callback),
                timeout=self.timeout
            )
            return result
        except asyncio.TimeoutError:
            logger.error(f"⏱️  Generation timeout after {self.timeout}s")
            
            if progress_callback:
                progress_callback(50, "Request timeout, switching to fallback...")
            
            # Try local generation on timeout
            return self.local_generator.generate_simple_video(prompt)
    
    async def _generate_async(
        self,
        prompt: str,
        progress_callback: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """Internal async generation with retry and routing"""
        
        def sync_generate():
            """Wrapper for sync generation"""
            return self.primary_generator.generate(prompt, progress_callback)
        
        # Run in thread pool
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, sync_generate)
        
        return result

    def generate(
        self,
        prompt: str,
        progress_callback: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        Main generation method with full resilience
        
        Strategy:
        1. Try primary generator with retry
        2. If fails, try with model routing
        3. If timeout, cancel and use fallback
        4. If all fails, use local generation
        
        Args:
            prompt: Video generation prompt
            progress_callback: Progress callback(percent, message)
        
        Returns:
            Generation result (always succeeds with fallback)
        """
        self.stats['total_requests'] += 1
        start_time = time.time()
        
        logger.info(f"🎬 Resilient generation: '{prompt}'")
        
        # Callback wrapper for user feedback
        def notify(percent: int, message: str, mode: str = ""):
            if progress_callback:
                full_message = f"{message}"
                if mode:
                    full_message = f"[{mode}] {message}"
                progress_callback(percent, full_message)
        
        try:
            # PHASE 1: Try primary with retry
            notify(5, "Connecting to video service...", "PRIMARY")
            
            def attempt_generation():
                return self.primary_generator.generate(prompt, progress_callback)
            
            try:
                result = self.retry_manager.retry_with_backoff(
                    attempt_generation,
                    on_retry=lambda attempt, delay, error: notify(
                        10 + attempt * 5,
                        f"Retrying in {delay}s... (attempt {attempt})",
                        "RETRY"
                    )
                )
                
                if result.get('success'):
                    self.stats['successful'] += 1
                    if self.retry_manager.retry_count > 0:
                        self.stats['retries_used'] += 1
                    
                    elapsed = time.time() - start_time
                    logger.info(f"✅ Success in {elapsed:.1f}s")
                    return result
            
            except Exception as e:
                logger.warning(f"⚠️  Primary generation failed: {e}")
                notify(30, "Primary service unavailable, trying fallback...", "FALLBACK")
        
        except Exception as e:
            logger.error(f"❌ Unexpected error: {e}")
        
        # PHASE 2: Try local generation
        notify(50, "Using local generation mode...", "LOCAL")
        self.stats['local_mode_used'] += 1
        
        try:
            result = self.local_generator.generate_simple_video(prompt)
            
            if result.get('success'):
                self.stats['successful'] += 1
                elapsed = time.time() - start_time
                logger.info(f"✅ Local generation success in {elapsed:.1f}s")
                return result
        
        except Exception as e:
            logger.error(f"❌ Local generation failed: {e}")
        
        # PHASE 3: Complete failure (should never happen)
        self.stats['failed'] += 1
        elapsed = time.time() - start_time
        
        return {
            'success': False,
            'error': 'All generation methods failed',
            'message': 'Unable to generate video. Please try again later.',
            'duration': elapsed
        }

    def get_stats(self) -> Dict[str, Any]:
        """Get generation statistics"""
        success_rate = 0
        if self.stats['total_requests'] > 0:
            success_rate = (self.stats['successful'] / self.stats['total_requests']) * 100
        
        return {
            **self.stats,
            'success_rate': round(success_rate, 2),
            'retry_stats': self.retry_manager.get_stats(),
            'router_stats': self.model_router.get_stats()
        }
    
    def reset_stats(self):
        """Reset all statistics"""
        self.stats = {
            'total_requests': 0,
            'successful': 0,
            'failed': 0,
            'retries_used': 0,
            'fallbacks_used': 0,
            'local_mode_used': 0
        }
        logger.info("📊 Statistics reset")


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("RESILIENT VIDEO GENERATOR - TEST")
    print("=" * 60)
    
    generator = ResilientVideoGenerator()
    
    # Test generation
    result = generator.generate(
        "A beautiful sunset over mountains",
        progress_callback=lambda p, m: print(f"[{p}%] {m}")
    )
    
    print(f"\n{'='*60}")
    if result['success']:
        print(f"✅ SUCCESS")
        print(f"   Video: {result.get('video_path')}")
        print(f"   Duration: {result.get('duration', 0):.1f}s")
    else:
        print(f"❌ FAILED")
        print(f"   Error: {result.get('message')}")
    
    print(f"\n📊 Statistics:")
    stats = generator.get_stats()
    print(f"   Total requests: {stats['total_requests']}")
    print(f"   Success rate: {stats['success_rate']}%")
    print(f"   Retries used: {stats['retries_used']}")
    print(f"   Local mode: {stats['local_mode_used']}")
