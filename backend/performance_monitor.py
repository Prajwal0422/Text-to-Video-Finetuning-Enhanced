"""
Performance Monitoring System
Real-time tracking of video generation metrics
"""

import time
import json
from typing import Dict, List, Optional
from datetime import datetime
from collections import deque
import threading

class PerformanceMonitor:
    def __init__(self, max_history: int = 100):
        self.max_history = max_history
        self.history = deque(maxlen=max_history)
        self.current_session = {}
        self.lock = threading.Lock()
        
        # Metrics
        self.total_generations = 0
        self.successful_generations = 0
        self.failed_generations = 0
        self.total_time = 0.0
        
    def start_generation(self, prompt: str, mode: str = "standard") -> str:
        """Start tracking a new generation"""
        session_id = f"{int(time.time() * 1000)}"
        
        with self.lock:
            self.current_session[session_id] = {
                'prompt': prompt,
                'mode': mode,
                'start_time': time.time(),
                'status': 'in_progress'
            }
        
        return session_id
    
    def end_generation(self, session_id: str, success: bool = True, 
                      output_path: Optional[str] = None, error: Optional[str] = None):
        """End tracking and record metrics"""
        with self.lock:
            if session_id not in self.current_session:
                return
            
            session = self.current_session[session_id]
            end_time = time.time()
            duration = end_time - session['start_time']
            
            # Update metrics
            self.total_generations += 1
            self.total_time += duration
            
            if success:
                self.successful_generations += 1
            else:
                self.failed_generations += 1
            
            # Record in history
            record = {
                'session_id': session_id,
                'prompt': session['prompt'],
                'mode': session['mode'],
                'duration': round(duration, 2),
                'success': success,
                'output_path': output_path,
                'error': error,
                'timestamp': datetime.now().isoformat()
            }
            
            self.history.append(record)
            
            # Remove from current sessions
            del self.current_session[session_id]
    
    def get_stats(self) -> Dict:
        """Get current performance statistics"""
        with self.lock:
            if self.total_generations == 0:
                return {
                    'total_generations': 0,
                    'success_rate': 0.0,
                    'avg_duration': 0.0,
                    'total_time': 0.0
                }
            
            success_rate = (self.successful_generations / self.total_generations) * 100
            avg_duration = self.total_time / self.total_generations
            
            # Calculate mode-specific stats
            mode_stats = {}
            for record in self.history:
                mode = record['mode']
                if mode not in mode_stats:
                    mode_stats[mode] = {'count': 0, 'total_time': 0.0, 'successes': 0}
                
                mode_stats[mode]['count'] += 1
                mode_stats[mode]['total_time'] += record['duration']
                if record['success']:
                    mode_stats[mode]['successes'] += 1
            
            # Calculate averages per mode
            for mode, stats in mode_stats.items():
                stats['avg_duration'] = round(stats['total_time'] / stats['count'], 2)
                stats['success_rate'] = round((stats['successes'] / stats['count']) * 100, 1)
            
            return {
                'total_generations': self.total_generations,
                'successful': self.successful_generations,
                'failed': self.failed_generations,
                'success_rate': round(success_rate, 1),
                'avg_duration': round(avg_duration, 2),
                'total_time': round(self.total_time, 2),
                'mode_stats': mode_stats,
                'active_sessions': len(self.current_session)
            }
    
    def get_recent_history(self, limit: int = 10) -> List[Dict]:
        """Get recent generation history"""
        with self.lock:
            return list(self.history)[-limit:]
    
    def get_performance_report(self) -> str:
        """Generate a formatted performance report"""
        stats = self.get_stats()
        
        report = []
        report.append("=" * 60)
        report.append("PERFORMANCE REPORT")
        report.append("=" * 60)
        report.append(f"Total Generations: {stats['total_generations']}")
        report.append(f"Successful: {stats['successful']}")
        report.append(f"Failed: {stats['failed']}")
        report.append(f"Success Rate: {stats['success_rate']}%")
        report.append(f"Average Duration: {stats['avg_duration']}s")
        report.append(f"Total Time: {stats['total_time']}s")
        report.append("")
        
        if stats['mode_stats']:
            report.append("Mode-Specific Stats:")
            report.append("-" * 60)
            for mode, mode_stat in stats['mode_stats'].items():
                report.append(f"{mode.upper()}:")
                report.append(f"  Count: {mode_stat['count']}")
                report.append(f"  Avg Duration: {mode_stat['avg_duration']}s")
                report.append(f"  Success Rate: {mode_stat['success_rate']}%")
                report.append("")
        
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def export_metrics(self, filepath: str):
        """Export metrics to JSON file"""
        with self.lock:
            data = {
                'stats': self.get_stats(),
                'history': list(self.history),
                'exported_at': datetime.now().isoformat()
            }
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
    
    def clear_history(self):
        """Clear all history (keeps current stats)"""
        with self.lock:
            self.history.clear()


# Global instance
monitor = PerformanceMonitor()


if __name__ == "__main__":
    # Test
    print("Performance Monitor Test")
    print("=" * 60)
    
    # Simulate generations
    session1 = monitor.start_generation("ocean waves", "fast")
    time.sleep(0.5)
    monitor.end_generation(session1, success=True, output_path="video1.mp4")
    
    session2 = monitor.start_generation("mountain sunset", "standard")
    time.sleep(0.8)
    monitor.end_generation(session2, success=True, output_path="video2.mp4")
    
    session3 = monitor.start_generation("city lights", "ultra_fast")
    time.sleep(0.3)
    monitor.end_generation(session3, success=False, error="API timeout")
    
    # Print report
    print(monitor.get_performance_report())
    
    # Recent history
    print("\nRecent History:")
    for record in monitor.get_recent_history(3):
        print(f"  {record['prompt'][:20]:20} | {record['mode']:12} | {record['duration']}s | {'✅' if record['success'] else '❌'}")
