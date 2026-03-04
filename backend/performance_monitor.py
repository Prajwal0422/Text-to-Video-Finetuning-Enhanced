"""
Performance Monitoring
Track and analyze video generation performance
"""

import time
import psutil
import logging
from typing import Dict, List
from collections import defaultdict

logger = logging.getLogger(__name__)


class PerformanceMonitor:
    """Monitor and track performance metrics"""
    
    def __init__(self):
        self.timers = {}
        self.metrics = defaultdict(list)
        self.start_times = {}
    
    def start_timer(self, operation: str):
        """Start timing an operation"""
        self.start_times[operation] = time.time()
    
    def end_timer(self, operation: str) -> float:
        """End timing and return duration"""
        if operation in self.start_times:
            duration = time.time() - self.start_times[operation]
            self.metrics[operation].append(duration)
            del self.start_times[operation]
            return duration
        return 0.0
    
    def record_metric(self, name: str, value: float):
        """Record a custom metric"""
        self.metrics[name].append(value)
    
    def get_average(self, operation: str) -> float:
        """Get average time for an operation"""
        if operation in self.metrics and len(self.metrics[operation]) > 0:
            return sum(self.metrics[operation]) / len(self.metrics[operation])
        return 0.0
    
    def get_total(self, operation: str) -> float:
        """Get total time for an operation"""
        if operation in self.metrics:
            return sum(self.metrics[operation])
        return 0.0
    
    def get_report(self) -> Dict:
        """Generate performance report"""
        report = {}
        
        for operation, times in self.metrics.items():
            if len(times) > 0:
                report[operation] = {
                    "count": len(times),
                    "total": sum(times),
                    "average": sum(times) / len(times),
                    "min": min(times),
                    "max": max(times)
                }
        
        return report
    
    def print_report(self):
        """Print formatted performance report"""
        report = self.get_report()
        
        logger.info("=" * 60)
        logger.info("PERFORMANCE REPORT")
        logger.info("=" * 60)
        
        for operation, stats in report.items():
            logger.info(f"\n{operation}:")
            logger.info(f"  Count: {stats['count']}")
            logger.info(f"  Total: {stats['total']:.3f}s")
            logger.info(f"  Average: {stats['average']:.3f}s")
            logger.info(f"  Min: {stats['min']:.3f}s")
            logger.info(f"  Max: {stats['max']:.3f}s")
        
        logger.info("=" * 60)
    
    def get_system_metrics(self) -> Dict:
        """Get current system resource usage"""
        return {
            "cpu_percent": psutil.cpu_percent(interval=0.1),
            "memory_percent": psutil.virtual_memory().percent,
            "memory_available_mb": psutil.virtual_memory().available / (1024 * 1024)
        }
    
    def reset(self):
        """Reset all metrics"""
        self.timers.clear()
        self.metrics.clear()
        self.start_times.clear()


class PerformanceProfiler:
    """Context manager for easy performance profiling"""
    
    def __init__(self, monitor: PerformanceMonitor, operation: str):
        self.monitor = monitor
        self.operation = operation
    
    def __enter__(self):
        self.monitor.start_timer(self.operation)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = self.monitor.end_timer(self.operation)
        logger.debug(f"{self.operation}: {duration:.3f}s")


# Global performance monitor
_global_monitor = None


def get_performance_monitor() -> PerformanceMonitor:
    """Get global performance monitor instance"""
    global _global_monitor
    if _global_monitor is None:
        _global_monitor = PerformanceMonitor()
    return _global_monitor
