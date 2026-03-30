"""
Video Analytics System
Track and analyze video generation patterns and user behavior
"""

import json
import time
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import os

class VideoAnalytics:
    def __init__(self, data_file: str = "outputs/analytics.json"):
        self.data_file = data_file
        self.data = self._load_data()
        
    def _load_data(self) -> Dict:
        """Load analytics data from file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            'total_generations': 0,
            'successful_generations': 0,
            'failed_generations': 0,
            'total_duration': 0.0,
            'prompts': [],
            'popular_keywords': {},
            'generation_times': [],
            'daily_stats': {}
        }
    
    def _save_data(self):
        """Save analytics data to file"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def track_generation(self, prompt: str, success: bool, duration: float, 
                        video_path: Optional[str] = None):
        """Track a video generation event"""
        self.data['total_generations'] += 1
        
        if success:
            self.data['successful_generations'] += 1
        else:
            self.data['failed_generations'] += 1
        
        self.data['total_duration'] += duration
        
        # Track prompt
        prompt_data = {
            'prompt': prompt,
            'success': success,
            'duration': duration,
            'timestamp': datetime.now().isoformat(),
            'video_path': video_path
        }
        self.data['prompts'].append(prompt_data)
        
        # Keep only last 1000 prompts
        if len(self.data['prompts']) > 1000:
            self.data['prompts'] = self.data['prompts'][-1000:]
        
        # Track keywords
        keywords = prompt.lower().split()
        for keyword in keywords:
            if len(keyword) > 3:
                self.data['popular_keywords'][keyword] = \
                    self.data['popular_keywords'].get(keyword, 0) + 1
        
        # Track generation time
        self.data['generation_times'].append(duration)
        if len(self.data['generation_times']) > 100:
            self.data['generation_times'] = self.data['generation_times'][-100:]
        
        # Track daily stats
        today = datetime.now().strftime('%Y-%m-%d')
        if today not in self.data['daily_stats']:
            self.data['daily_stats'][today] = {
                'total': 0,
                'successful': 0,
                'failed': 0
            }
        
        self.data['daily_stats'][today]['total'] += 1
        if success:
            self.data['daily_stats'][today]['successful'] += 1
        else:
            self.data['daily_stats'][today]['failed'] += 1
        
        self._save_data()
    
    def get_stats(self) -> Dict:
        """Get analytics statistics"""
        total = self.data['total_generations']
        
        if total == 0:
            return {
                'total_generations': 0,
                'success_rate': 0,
                'avg_duration': 0,
                'popular_keywords': []
            }
        
        success_rate = (self.data['successful_generations'] / total) * 100
        avg_duration = self.data['total_duration'] / total
        
        # Get top keywords
        sorted_keywords = sorted(
            self.data['popular_keywords'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        # Calculate recent performance
        recent_times = self.data['generation_times'][-20:]
        recent_avg = sum(recent_times) / len(recent_times) if recent_times else 0
        
        return {
            'total_generations': total,
            'successful': self.data['successful_generations'],
            'failed': self.data['failed_generations'],
            'success_rate': round(success_rate, 2),
            'avg_duration': round(avg_duration, 2),
            'recent_avg_duration': round(recent_avg, 2),
            'popular_keywords': sorted_keywords,
            'total_prompts': len(self.data['prompts'])
        }
    
    def get_popular_prompts(self, limit: int = 10) -> List[Dict]:
        """Get most popular prompts"""
        prompt_counts = defaultdict(int)
        prompt_data = {}
        
        for entry in self.data['prompts']:
            prompt = entry['prompt']
            prompt_counts[prompt] += 1
            if prompt not in prompt_data:
                prompt_data[prompt] = entry
        
        sorted_prompts = sorted(
            prompt_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:limit]
        
        return [
            {
                'prompt': prompt,
                'count': count,
                'last_used': prompt_data[prompt]['timestamp']
            }
            for prompt, count in sorted_prompts
        ]
    
    def get_daily_report(self, days: int = 7) -> Dict:
        """Get daily statistics for last N days"""
        today = datetime.now()
        report = {}
        
        for i in range(days):
            date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
            if date in self.data['daily_stats']:
                report[date] = self.data['daily_stats'][date]
            else:
                report[date] = {'total': 0, 'successful': 0, 'failed': 0}
        
        return report
    
    def get_analytics_report(self) -> str:
        """Generate formatted analytics report"""
        stats = self.get_stats()
        
        report = []
        report.append("=" * 60)
        report.append("VIDEO ANALYTICS REPORT")
        report.append("=" * 60)
        report.append(f"Total Generations: {stats['total_generations']}")
        report.append(f"Successful: {stats['successful']}")
        report.append(f"Failed: {stats['failed']}")
        report.append(f"Success Rate: {stats['success_rate']}%")
        report.append(f"Average Duration: {stats['avg_duration']}s")
        report.append(f"Recent Average: {stats['recent_avg_duration']}s")
        report.append("")
        
        if stats['popular_keywords']:
            report.append("Top Keywords:")
            for keyword, count in stats['popular_keywords'][:5]:
                report.append(f"  {keyword}: {count} times")
            report.append("")
        
        popular = self.get_popular_prompts(5)
        if popular:
            report.append("Popular Prompts:")
            for item in popular:
                report.append(f"  '{item['prompt'][:40]}...' ({item['count']} times)")
            report.append("")
        
        report.append("=" * 60)
        
        return "\n".join(report)


# Global instance
analytics = VideoAnalytics()


if __name__ == "__main__":
    print("Video Analytics Test")
    print("=" * 60)
    
    # Simulate some data
    analytics.track_generation("ocean waves", True, 18.5, "video1.mp4")
    analytics.track_generation("mountain sunset", True, 20.2, "video2.mp4")
    analytics.track_generation("city traffic", False, 15.0, None)
    
    # Print report
    print(analytics.get_analytics_report())
