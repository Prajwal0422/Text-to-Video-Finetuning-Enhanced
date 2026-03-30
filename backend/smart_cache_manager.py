"""
Smart Cache Manager
Intelligent caching with predictive pre-loading and optimization
"""

import os
import json
import time
from typing import Dict, List, Optional, Set
from collections import defaultdict
import hashlib

class SmartCacheManager:
    def __init__(self, cache_dir: str = "outputs/smart_cache"):
        self.cache_dir = cache_dir
        self.metadata_file = os.path.join(cache_dir, "smart_cache.json")
        os.makedirs(cache_dir, exist_ok=True)
        
        self.metadata = self._load_metadata()
        self.access_patterns = defaultdict(list)
        
    def _load_metadata(self) -> Dict:
        """Load cache metadata"""
        if os.path.exists(self.metadata_file):
            try:
                with open(self.metadata_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            'entries': {},
            'access_patterns': {},
            'predictions': {}
        }
    
    def _save_metadata(self):
        """Save cache metadata"""
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)
    
    def _get_cache_key(self, prompt: str) -> str:
        """Generate cache key"""
        return hashlib.md5(prompt.lower().strip().encode()).hexdigest()
    
    def record_access(self, prompt: str):
        """Record cache access for pattern learning"""
        cache_key = self._get_cache_key(prompt)
        timestamp = time.time()
        
        if cache_key not in self.metadata['access_patterns']:
            self.metadata['access_patterns'][cache_key] = []
        
        self.metadata['access_patterns'][cache_key].append(timestamp)
        
        # Keep only last 100 accesses
        if len(self.metadata['access_patterns'][cache_key]) > 100:
            self.metadata['access_patterns'][cache_key] = \
                self.metadata['access_patterns'][cache_key][-100:]
        
        self._save_metadata()
    
    def predict_next_prompts(self, current_prompt: str, limit: int = 5) -> List[str]:
        """Predict likely next prompts based on patterns"""
        # Extract keywords from current prompt
        keywords = set(current_prompt.lower().split())
        
        # Find prompts with similar keywords
        similar_prompts = []
        
        for cache_key, accesses in self.metadata['access_patterns'].items():
            if cache_key in self.metadata['entries']:
                entry = self.metadata['entries'][cache_key]
                prompt = entry.get('prompt', '')
                
                # Calculate keyword overlap
                prompt_keywords = set(prompt.lower().split())
                overlap = len(keywords & prompt_keywords)
                
                if overlap > 0:
                    # Weight by access frequency and recency
                    frequency = len(accesses)
                    recency = max(accesses) if accesses else 0
                    score = overlap * frequency * (1 + recency / time.time())
                    
                    similar_prompts.append((prompt, score))
        
        # Sort by score and return top predictions
        similar_prompts.sort(key=lambda x: x[1], reverse=True)
        
        return [prompt for prompt, score in similar_prompts[:limit]]
    
    def get_hot_cache_items(self, limit: int = 10) -> List[Dict]:
        """Get most frequently accessed cache items"""
        items = []
        
        for cache_key, entry in self.metadata['entries'].items():
            if cache_key in self.metadata['access_patterns']:
                accesses = self.metadata['access_patterns'][cache_key]
                
                # Calculate hotness score
                frequency = len(accesses)
                recent_accesses = [a for a in accesses if time.time() - a < 3600]  # Last hour
                recency_score = len(recent_accesses)
                
                hotness = frequency + (recency_score * 10)
                
                items.append({
                    'prompt': entry.get('prompt', ''),
                    'cache_key': cache_key,
                    'total_accesses': frequency,
                    'recent_accesses': recency_score,
                    'hotness': hotness
                })
        
        items.sort(key=lambda x: x['hotness'], reverse=True)
        return items[:limit]
    
    def suggest_preload(self) -> List[str]:
        """Suggest prompts to preload based on patterns"""
        hot_items = self.get_hot_cache_items(5)
        suggestions = []
        
        for item in hot_items:
            # Predict related prompts
            predictions = self.predict_next_prompts(item['prompt'], 3)
            suggestions.extend(predictions)
        
        # Remove duplicates
        return list(set(suggestions))[:10]
    
    def get_cache_efficiency(self) -> Dict:
        """Calculate cache efficiency metrics"""
        total_entries = len(self.metadata['entries'])
        total_accesses = sum(
            len(accesses) 
            for accesses in self.metadata['access_patterns'].values()
        )
        
        if total_entries == 0:
            return {
                'total_entries': 0,
                'total_accesses': 0,
                'avg_accesses_per_entry': 0,
                'cache_hit_rate': 0
            }
        
        avg_accesses = total_accesses / total_entries
        
        # Calculate hit rate (entries with > 1 access)
        hits = sum(
            1 for accesses in self.metadata['access_patterns'].values()
            if len(accesses) > 1
        )
        hit_rate = (hits / total_entries) * 100 if total_entries > 0 else 0
        
        return {
            'total_entries': total_entries,
            'total_accesses': total_accesses,
            'avg_accesses_per_entry': round(avg_accesses, 2),
            'cache_hit_rate': round(hit_rate, 2)
        }
    
    def optimize_cache(self):
        """Remove cold cache items to optimize storage"""
        current_time = time.time()
        cold_threshold = 7 * 24 * 3600  # 7 days
        
        cold_items = []
        
        for cache_key, accesses in self.metadata['access_patterns'].items():
            if not accesses:
                cold_items.append(cache_key)
                continue
            
            last_access = max(accesses)
            if current_time - last_access > cold_threshold:
                cold_items.append(cache_key)
        
        # Remove cold items
        for cache_key in cold_items:
            if cache_key in self.metadata['entries']:
                del self.metadata['entries'][cache_key]
            if cache_key in self.metadata['access_patterns']:
                del self.metadata['access_patterns'][cache_key]
        
        self._save_metadata()
        
        return len(cold_items)
    
    def get_report(self) -> str:
        """Generate smart cache report"""
        efficiency = self.get_cache_efficiency()
        hot_items = self.get_hot_cache_items(5)
        suggestions = self.suggest_preload()
        
        report = []
        report.append("=" * 60)
        report.append("SMART CACHE REPORT")
        report.append("=" * 60)
        report.append(f"Total Entries: {efficiency['total_entries']}")
        report.append(f"Total Accesses: {efficiency['total_accesses']}")
        report.append(f"Avg Accesses/Entry: {efficiency['avg_accesses_per_entry']}")
        report.append(f"Cache Hit Rate: {efficiency['cache_hit_rate']}%")
        report.append("")
        
        if hot_items:
            report.append("Hot Cache Items:")
            for item in hot_items:
                report.append(f"  '{item['prompt'][:40]}...'")
                report.append(f"    Accesses: {item['total_accesses']} (Recent: {item['recent_accesses']})")
            report.append("")
        
        if suggestions:
            report.append("Preload Suggestions:")
            for suggestion in suggestions[:5]:
                report.append(f"  - {suggestion[:50]}")
            report.append("")
        
        report.append("=" * 60)
        
        return "\n".join(report)


# Global instance
smart_cache = SmartCacheManager()


if __name__ == "__main__":
    print("Smart Cache Manager Test")
    print("=" * 60)
    
    # Simulate access patterns
    smart_cache.record_access("ocean waves")
    smart_cache.record_access("ocean sunset")
    smart_cache.record_access("ocean waves")
    
    # Print report
    print(smart_cache.get_report())
