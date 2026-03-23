"""
Video Metadata Manager
Extracts and manages video metadata
"""

import os
import json
from typing import Dict, Optional
from datetime import datetime
from moviepy import VideoFileClip
import hashlib

class VideoMetadataManager:
    """Manages video metadata and information"""
    
    def __init__(self, metadata_dir: str = "outputs/metadata"):
        self.metadata_dir = metadata_dir
        os.makedirs(metadata_dir, exist_ok=True)
    
    def extract_metadata(self, video_path: str) -> Dict:
        """
        Extract metadata from video file
        
        Args:
            video_path: Path to video file
        
        Returns:
            Dictionary with video metadata
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video not found: {video_path}")
        
        # Get file info
        file_size = os.path.getsize(video_path)
        file_hash = self._calculate_hash(video_path)
        created_time = os.path.getctime(video_path)
        
        # Extract video properties
        clip = VideoFileClip(video_path)
        
        metadata = {
            'file': {
                'path': video_path,
                'filename': os.path.basename(video_path),
                'size_bytes': file_size,
                'size_mb': round(file_size / (1024 * 1024), 2),
                'hash': file_hash,
                'created': datetime.fromtimestamp(created_time).isoformat()
            },
            'video': {
                'duration': round(clip.duration, 2),
                'width': clip.w,
                'height': clip.h,
                'fps': clip.fps,
                'resolution': f"{clip.w}x{clip.h}",
                'aspect_ratio': round(clip.w / clip.h, 2) if clip.h > 0 else 0
            },
            'extracted_at': datetime.now().isoformat()
        }
        
        clip.close()
        
        return metadata
    
    def _calculate_hash(self, file_path: str, chunk_size: int = 8192) -> str:
        """Calculate MD5 hash of file"""
        md5 = hashlib.md5()
        
        with open(file_path, 'rb') as f:
            while chunk := f.read(chunk_size):
                md5.update(chunk)
        
        return md5.hexdigest()
    
    def save_metadata(self, video_path: str, additional_data: Optional[Dict] = None) -> str:
        """
        Save metadata to JSON file
        
        Args:
            video_path: Path to video file
            additional_data: Additional metadata to include
        
        Returns:
            Path to metadata file
        """
        # Extract metadata
        metadata = self.extract_metadata(video_path)
        
        # Add additional data
        if additional_data:
            metadata['additional'] = additional_data
        
        # Generate metadata filename
        video_basename = os.path.splitext(os.path.basename(video_path))[0]
        metadata_filename = f"{video_basename}_metadata.json"
        metadata_path = os.path.join(self.metadata_dir, metadata_filename)
        
        # Save to file
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return metadata_path
    
    def load_metadata(self, video_path: str) -> Optional[Dict]:
        """Load metadata from JSON file"""
        video_basename = os.path.splitext(os.path.basename(video_path))[0]
        metadata_filename = f"{video_basename}_metadata.json"
        metadata_path = os.path.join(self.metadata_dir, metadata_filename)
        
        if not os.path.exists(metadata_path):
            return None
        
        with open(metadata_path, 'r') as f:
            return json.load(f)
    
    def get_video_info(self, video_path: str) -> Dict:
        """
        Get comprehensive video information
        
        Args:
            video_path: Path to video file
        
        Returns:
            Dictionary with video information
        """
        # Try to load cached metadata
        cached = self.load_metadata(video_path)
        
        if cached:
            return cached
        
        # Extract fresh metadata
        return self.extract_metadata(video_path)
    
    def compare_videos(self, video_path1: str, video_path2: str) -> Dict:
        """Compare two videos"""
        meta1 = self.extract_metadata(video_path1)
        meta2 = self.extract_metadata(video_path2)
        
        return {
            'video1': meta1,
            'video2': meta2,
            'comparison': {
                'same_resolution': meta1['video']['resolution'] == meta2['video']['resolution'],
                'same_duration': abs(meta1['video']['duration'] - meta2['video']['duration']) < 0.1,
                'same_fps': meta1['video']['fps'] == meta2['video']['fps'],
                'size_difference_mb': abs(meta1['file']['size_mb'] - meta2['file']['size_mb'])
            }
        }
    
    def get_all_metadata(self) -> list:
        """Get metadata for all videos in metadata directory"""
        metadata_files = [f for f in os.listdir(self.metadata_dir) if f.endswith('_metadata.json')]
        
        all_metadata = []
        for filename in metadata_files:
            filepath = os.path.join(self.metadata_dir, filename)
            with open(filepath, 'r') as f:
                all_metadata.append(json.load(f))
        
        return all_metadata


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("VIDEO METADATA MANAGER - TEST")
    print("=" * 60)
    
    manager = VideoMetadataManager()
    
    # Test with existing video
    test_video = "outputs/videos/video_273973db.mp4"
    
    if os.path.exists(test_video):
        print(f"\nExtracting metadata from: {test_video}")
        
        metadata = manager.extract_metadata(test_video)
        
        print("\nFile Information:")
        print(f"  Filename: {metadata['file']['filename']}")
        print(f"  Size: {metadata['file']['size_mb']} MB")
        print(f"  Hash: {metadata['file']['hash']}")
        
        print("\nVideo Properties:")
        print(f"  Duration: {metadata['video']['duration']}s")
        print(f"  Resolution: {metadata['video']['resolution']}")
        print(f"  FPS: {metadata['video']['fps']}")
        print(f"  Aspect Ratio: {metadata['video']['aspect_ratio']}")
        
        # Save metadata
        metadata_path = manager.save_metadata(test_video, {
            'prompt': 'ocean waves on beach',
            'generation_time': 29.3
        })
        
        print(f"\n✅ Metadata saved to: {metadata_path}")
    else:
        print(f"\n⚠️  Test video not found: {test_video}")
