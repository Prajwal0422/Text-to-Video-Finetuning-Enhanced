"""
Analytics Tracker
Tracks user behavior and system performance for insights
"""

import time
import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict

class AnalyticsTracker:
    """Tracks analytics for video generation system"""
    
    def __init__(self, storage_file: str = "analytics_data.json"):
        self.storage_file = storage_file
        self.events: List[Dict] = []
        self.session_start = time.time()
        self.load_data()
    
    def load_data(self):
        """Load analytics data from file"""
        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
                self.events = data.get('events', [])
        except FileNotFoundError:
            self.events = []
    
    def save_data(self):
        """Save analytics data to file"""
        data = {
            'events': self.events[-1000:],  # Keep last 1000 events
            'last_updated': datetime.now().isoformat()
        }
        with open(self.storage_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def track_event(
        self,
        event_type: str,
        properties: Optional[Dict] = None
    ):
        """Track an analytics event"""
        event = {
            'type': event_type,
            'timestamp': time.time(),
            'datetime': datetime.now().isoformat(),
            'properties': properties or {}
        }
        self.events.append(event)
        
        # Auto-save every 10 events
        if len(self.events) % 10 == 0:
            self.save_data()
    
    def track_generation(
        self,
        prompt: str,
        duration: float,
        success: bool,
        file_size: Optional[int] = None,
        error: Optional[str] = None
    ):
        """Track a video generation event"""
        self.track_event('video_generation', {
            'prompt': prompt[:100],  # Truncate long prompts
            'duration': duration,
            'success': success,
            'file_size': file_size,
            'error': error
        })
    
    def track_user_action(
        self,
        action: str,
        details: Optional[Dict] = None
    ):
        """Track a user action"""
        self.track_event('user_action', {
            'action': action,
            'details': details or {}
        })
    
    def get_stats(self, hours: int = 24) -> Dict:
        """Get analytics statistics for last N hours"""
        cutoff_time = time.time() - (hours * 3600)
        recent_events = [e for e in self.events if e['timestamp'] > cutoff_time]
        
        # Count by event type
        event_counts = defaultdict(int)
        for event in recent_events:
            event_counts[event['type']] += 1
        
        # Video generation stats
        gen_events = [e for e in recent_events if e['type'] == 'video_generation']
        successful = sum(1 for e in gen_events if e['properties'].get('success'))
        failed = len(gen_events) - successful
        
        avg_duration = 0
        if gen_events:
            avg_duration = sum(e['properties'].get('duration', 0) for e in gen_events) / len(gen_events)
        
        # Popular prompts
        prompt_counts = defaultdict(int)
        for event in gen_events:
            prompt = event['properties'].get('prompt', '')
            if prompt:
                prompt_counts[prompt] += 1
        
        top_prompts = sorted(prompt_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            'period_hours': hours,
            'total_events': len(recent_events),
            'event_counts': dict(event_counts),
            'video_generation': {
                'total': len(gen_events),
                'successful': successful,
                'failed': failed,
                'success_rate': (successful / len(gen_events) * 100) if gen_events else 0,
                'avg_duration': round(avg_duration, 2)
            },
            'top_prompts': [{'prompt': p, 'count': c} for p, c in top_prompts]
        }
    
    def get_hourly_breakdown(self, hours: int = 24) -> List[Dict]:
        """Get hourly breakdown of activity"""
        cutoff_time = time.time() - (hours * 3600)
        recent_events = [e for e in self.events if e['timestamp'] > cutoff_time]
        
        # Group by hour
        hourly_data = defaultdict(lambda: {'total': 0, 'successful': 0, 'failed': 0})
        
        for event in recent_events:
            if event['type'] == 'video_generation':
                hour = datetime.fromtimestamp(event['timestamp']).strftime('%Y-%m-%d %H:00')
                hourly_data[hour]['total'] += 1
                if event['properties'].get('success'):
                    hourly_data[hour]['successful'] += 1
                else:
                    hourly_data[hour]['failed'] += 1
        
        # Convert to list
        breakdown = []
        for hour in sorted(hourly_data.keys()):
            data = hourly_data[hour]
            breakdown.append({
                'hour': hour,
                'total': data['total'],
                'successful': data['successful'],
                'failed': data['failed']
            })
        
        return breakdown
    
    def get_performance_metrics(self) -> Dict:
        """Get system performance metrics"""
        gen_events = [e for e in self.events if e['type'] == 'video_generation']
        
        if not gen_events:
            return {'message': 'No data available'}
        
        durations = [e['properties'].get('duration', 0) for e in gen_events]
        successful = [e for e in gen_events if e['properties'].get('success')]
        
        return {
            'total_generations': len(gen_events),
            'successful': len(successful),
            'failed': len(gen_events) - len(successful),
            'avg_duration': round(sum(durations) / len(durations), 2),
            'min_duration': round(min(durations), 2),
            'max_duration': round(max(durations), 2),
            'success_rate': round(len(successful) / len(gen_events) * 100, 2)
        }


# Example usage
if __name__ == "__main__":
    tracker = AnalyticsTracker()
    
    # Simulate some events
    tracker.track_generation("ocean waves", 25.3, True, 2500000)
    tracker.track_generation("mountain sunset", 28.1, True, 2800000)
    tracker.track_generation("city night", 15.2, False, error="Timeout")
    
    # Get stats
    stats = tracker.get_stats(24)
    print("Analytics Stats:")
    print(json.dumps(stats, indent=2))
    
    # Get performance metrics
    metrics = tracker.get_performance_metrics()
    print("\nPerformance Metrics:")
    print(json.dumps(metrics, indent=2))
