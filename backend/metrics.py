"""
Performance Metrics Tracking
Monitors system performance and generation statistics
"""

import time
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class GenerationMetric:
    """Single generation metric"""
    timestamp: float
    prompt: str
    duration: float
    success: bool
    method: str  # 'primary', 'retry', 'fallback', 'local'
    error: Optional[str] = None

class MetricsCollector:
    """Collects and analyzes performance metrics"""
    
    def __init__(self):
        self.metrics: List[GenerationMetric] = []
        self.start_time = time.time()
    
    def record_generation(
        self,
        prompt: str,
        duration: float,
        success: bool,
        method: str,
        error: Optional[str] = None
    ):
        """Record a generation attempt"""
        metric = GenerationMetric(
            timestamp=time.time(),
            prompt=prompt,
            duration=duration,
            success=success,
            method=method,
            error=error
        )
        self.metrics.append(metric)
    
    def get_stats(self) -> Dict:
        """Get comprehensive statistics"""
        if not self.metrics:
            return {
                'total_generations': 0,
                'success_rate': 0,
                'avg_duration': 0,
                'uptime': time.time() - self.start_time
            }
        
        total = len(self.metrics)
        successful = sum(1 for m in self.metrics if m.success)
        failed = total - successful
        
        success_rate = (successful / total * 100) if total > 0 else 0
        
        # Calculate average duration for successful generations
        successful_durations = [m.duration for m in self.metrics if m.success]
        avg_duration = sum(successful_durations) / len(successful_durations) if successful_durations else 0
        
        # Method breakdown
        methods = {}
        for m in self.metrics:
            methods[m.method] = methods.get(m.method, 0) + 1
        
        return {
            'total_generations': total,
            'successful': successful,
            'failed': failed,
            'success_rate': round(success_rate, 2),
            'avg_duration': round(avg_duration, 2),
            'methods': methods,
            'uptime': round(time.time() - self.start_time, 2)
        }
    
    def get_recent(self, count: int = 10) -> List[Dict]:
        """Get recent generation attempts"""
        recent = self.metrics[-count:]
        return [
            {
                'timestamp': datetime.fromtimestamp(m.timestamp).isoformat(),
                'prompt': m.prompt[:50] + '...' if len(m.prompt) > 50 else m.prompt,
                'duration': round(m.duration, 2),
                'success': m.success,
                'method': m.method,
                'error': m.error
            }
            for m in recent
        ]
    
    def reset(self):
        """Reset all metrics"""
        self.metrics.clear()
        self.start_time = time.time()

# Global metrics collector
metrics = MetricsCollector()
