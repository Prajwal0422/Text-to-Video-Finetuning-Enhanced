"""
NEXUS VISION - Clip Ranking System
Scores and ranks video clips based on multiple criteria
"""

from typing import List, Dict, Tuple
import re

class ClipRanker:
    def __init__(self):
        self.weights = {
            'keyword_similarity': 10.0,  # Most important
            'duration': 5.0,
            'resolution': 3.0,
            'orientation': 2.0
        }
    
    def calculate_keyword_similarity(self, query: str, video: Dict) -> float:
        """Calculate keyword match score"""
        query_words = set(query.lower().split())
        
        # Get video metadata
        tags = video.get('tags', [])
        if isinstance(tags, str):
            tags = [tags]
        
        # Convert tags to lowercase
        video_tags = set()
        for tag in tags:
            if isinstance(tag, str):
                video_tags.update(tag.lower().split())
        
        # Calculate matches
        if not query_words or not video_tags:
            return 0.0
        
        # Exact matches
        exact_matches = len(query_words & video_tags)
        
        # Partial matches (substring)
        partial_matches = 0
        for q_word in query_words:
            for v_tag in video_tags:
                if q_word in v_tag or v_tag in q_word:
                    partial_matches += 0.5
                    break
        
        # Calculate score (0-10)
        total_matches = exact_matches + partial_matches
        max_possible = len(query_words)
        
        if max_possible == 0:
            return 0.0
        
        score = (total_matches / max_possible) * 10.0
        return min(score, 10.0)
    
    def calculate_duration_score(self, video: Dict) -> float:
        """Score based on video duration (prefer 4-10 seconds)"""
        duration = video.get('duration', 0)
        
        if duration == 0:
            return 0.0
        
        # Ideal range: 4-10 seconds
        if 4 <= duration <= 10:
            return 10.0
        elif 3 <= duration < 4:
            return 7.0
        elif 10 < duration <= 15:
            return 7.0
        elif 2 <= duration < 3:
            return 5.0
        elif 15 < duration <= 20:
            return 5.0
        else:
            return 3.0
    
    def calculate_resolution_score(self, video_file: Dict) -> float:
        """Score based on resolution (prefer HD but not too large)"""
        width = video_file.get('width', 0)
        height = video_file.get('height', 0)
        
        if width == 0 or height == 0:
            return 0.0
        
        # Calculate total pixels
        pixels = width * height
        
        # Scoring based on resolution
        if 1280 <= width <= 1920:  # 720p to 1080p (ideal)
            return 10.0
        elif 640 <= width < 1280:  # SD to 720p
            return 7.0
        elif width >= 1920:  # Above 1080p (too large)
            return 5.0
        else:  # Below SD
            return 3.0
    
    def calculate_orientation_score(self, video_file: Dict) -> float:
        """Score based on orientation (prefer landscape)"""
        width = video_file.get('width', 0)
        height = video_file.get('height', 0)
        
        if width == 0 or height == 0:
            return 5.0  # Neutral if unknown
        
        aspect_ratio = width / height
        
        # Landscape (16:9, 16:10, etc.)
        if aspect_ratio >= 1.5:
            return 10.0
        # Square-ish
        elif 0.9 <= aspect_ratio < 1.5:
            return 5.0
        # Portrait
        else:
            return 2.0
    
    def rank_video_file(self, video_file: Dict, query: str, video: Dict) -> Tuple[float, Dict]:
        """Rank a single video file"""
        scores = {
            'keyword_similarity': self.calculate_keyword_similarity(query, video),
            'duration': self.calculate_duration_score(video),
            'resolution': self.calculate_resolution_score(video_file),
            'orientation': self.calculate_orientation_score(video_file)
        }
        
        # Calculate weighted total
        total_score = sum(
            scores[criterion] * self.weights[criterion]
            for criterion in scores
        )
        
        # Normalize to 0-100
        max_score = sum(10.0 * weight for weight in self.weights.values())
        normalized_score = (total_score / max_score) * 100.0
        
        return normalized_score, {
            'video_file': video_file,
            'video': video,
            'score': normalized_score,
            'breakdown': scores
        }
    
    def rank_videos(self, videos: List[Dict], query: str) -> List[Dict]:
        """Rank all videos and their files"""
        ranked_results = []
        
        for video in videos:
            video_files = video.get('video_files', [])
            
            if not video_files:
                continue
            
            # Rank each video file
            for video_file in video_files:
                score, result = self.rank_video_file(video_file, query, video)
                ranked_results.append(result)
        
        # Sort by score (highest first)
        ranked_results.sort(key=lambda x: x['score'], reverse=True)
        
        return ranked_results
    
    def get_best_clip(self, videos: List[Dict], query: str) -> Dict:
        """Get the single best clip"""
        ranked = self.rank_videos(videos, query)
        
        if not ranked:
            return None
        
        return ranked[0]
    
    def get_top_clips(self, videos: List[Dict], query: str, n: int = 3) -> List[Dict]:
        """Get top N clips"""
        ranked = self.rank_videos(videos, query)
        return ranked[:n]


if __name__ == "__main__":
    # Test the ranker
    ranker = ClipRanker()
    
    # Mock video data
    test_videos = [
        {
            'id': 1,
            'tags': ['car', 'traffic', 'highway', 'busy'],
            'duration': 8,
            'video_files': [
                {'width': 1280, 'height': 720, 'link': 'video1.mp4'},
                {'width': 640, 'height': 480, 'link': 'video1_sd.mp4'}
            ]
        },
        {
            'id': 2,
            'tags': ['nature', 'landscape'],
            'duration': 15,
            'video_files': [
                {'width': 1920, 'height': 1080, 'link': 'video2.mp4'}
            ]
        },
        {
            'id': 3,
            'tags': ['car', 'driving', 'road'],
            'duration': 5,
            'video_files': [
                {'width': 1280, 'height': 720, 'link': 'video3.mp4'}
            ]
        }
    ]
    
    query = "car traffic highway"
    
    print(f"Query: {query}")
    print("="*70)
    
    ranked = ranker.rank_videos(test_videos, query)
    
    for i, result in enumerate(ranked[:5], 1):
        print(f"\nRank {i}: Score {result['score']:.1f}")
        print(f"  Video ID: {result['video']['id']}")
        print(f"  Tags: {result['video']['tags']}")
        print(f"  Resolution: {result['video_file']['width']}x{result['video_file']['height']}")
        print(f"  Duration: {result['video']['duration']}s")
        print(f"  Breakdown: {result['breakdown']}")
