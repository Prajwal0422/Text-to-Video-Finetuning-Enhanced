"""
Video Quality Analyzer
Analyzes generated videos for quality metrics
"""

import os
from typing import Dict, Optional
from moviepy import VideoFileClip
import numpy as np

class QualityAnalyzer:
    def __init__(self):
        self.quality_thresholds = {
            'min_duration': 5.0,  # seconds
            'max_duration': 60.0,
            'min_resolution': (480, 270),  # 480p
            'target_resolution': (640, 360),
            'min_fps': 20,
            'target_fps': 24,
            'min_bitrate': 500,  # kbps
        }
    
    def analyze_video(self, video_path: str) -> Dict:
        """Analyze video and return quality metrics"""
        if not os.path.exists(video_path):
            return {'error': 'File not found', 'quality_score': 0}
        
        try:
            clip = VideoFileClip(video_path)
            
            # Basic metrics
            duration = clip.duration
            width = clip.w
            height = clip.h
            fps = clip.fps
            file_size = os.path.getsize(video_path)
            
            # Calculate bitrate (approximate)
            bitrate_kbps = (file_size * 8) / (duration * 1000) if duration > 0 else 0
            
            # Quality scoring
            quality_score = self._calculate_quality_score(
                duration, width, height, fps, bitrate_kbps
            )
            
            # Frame analysis (sample)
            frame_quality = self._analyze_frames(clip)
            
            clip.close()
            
            return {
                'duration': round(duration, 2),
                'resolution': f"{width}x{height}",
                'width': width,
                'height': height,
                'fps': fps,
                'file_size_mb': round(file_size / (1024 * 1024), 2),
                'bitrate_kbps': round(bitrate_kbps, 2),
                'quality_score': quality_score,
                'frame_quality': frame_quality,
                'passes_quality_check': quality_score >= 70
            }
            
        except Exception as e:
            return {'error': str(e), 'quality_score': 0}
    
    def _calculate_quality_score(self, duration: float, width: int, 
                                 height: int, fps: float, bitrate: float) -> int:
        """Calculate overall quality score (0-100)"""
        score = 0
        
        # Duration score (20 points)
        if self.quality_thresholds['min_duration'] <= duration <= self.quality_thresholds['max_duration']:
            score += 20
        elif duration > 0:
            score += 10
        
        # Resolution score (30 points)
        target_w, target_h = self.quality_thresholds['target_resolution']
        min_w, min_h = self.quality_thresholds['min_resolution']
        
        if width >= target_w and height >= target_h:
            score += 30
        elif width >= min_w and height >= min_h:
            score += 20
        else:
            score += 10
        
        # FPS score (20 points)
        if fps >= self.quality_thresholds['target_fps']:
            score += 20
        elif fps >= self.quality_thresholds['min_fps']:
            score += 15
        else:
            score += 5
        
        # Bitrate score (30 points)
        if bitrate >= 1000:  # Good quality
            score += 30
        elif bitrate >= self.quality_thresholds['min_bitrate']:
            score += 20
        else:
            score += 10
        
        return min(score, 100)
    
    def _analyze_frames(self, clip: VideoFileClip, sample_count: int = 5) -> Dict:
        """Analyze sample frames for quality"""
        try:
            duration = clip.duration
            if duration <= 0:
                return {'error': 'Invalid duration'}
            
            # Sample frames at regular intervals
            sample_times = np.linspace(0, duration - 0.1, sample_count)
            
            brightness_values = []
            contrast_values = []
            
            for t in sample_times:
                frame = clip.get_frame(t)
                
                # Convert to grayscale for analysis
                gray = np.mean(frame, axis=2)
                
                # Brightness (mean pixel value)
                brightness = np.mean(gray)
                brightness_values.append(brightness)
                
                # Contrast (standard deviation)
                contrast = np.std(gray)
                contrast_values.append(contrast)
            
            avg_brightness = np.mean(brightness_values)
            avg_contrast = np.mean(contrast_values)
            
            # Quality assessment
            brightness_quality = "good" if 50 <= avg_brightness <= 200 else "poor"
            contrast_quality = "good" if avg_contrast > 20 else "poor"
            
            return {
                'avg_brightness': round(float(avg_brightness), 2),
                'avg_contrast': round(float(avg_contrast), 2),
                'brightness_quality': brightness_quality,
                'contrast_quality': contrast_quality,
                'samples_analyzed': sample_count
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def generate_quality_report(self, video_path: str) -> str:
        """Generate formatted quality report"""
        metrics = self.analyze_video(video_path)
        
        if 'error' in metrics:
            return f"❌ Error analyzing video: {metrics['error']}"
        
        report = []
        report.append("=" * 60)
        report.append("VIDEO QUALITY REPORT")
        report.append("=" * 60)
        report.append(f"File: {os.path.basename(video_path)}")
        report.append("")
        report.append("Basic Metrics:")
        report.append(f"  Duration: {metrics['duration']}s")
        report.append(f"  Resolution: {metrics['resolution']}")
        report.append(f"  FPS: {metrics['fps']}")
        report.append(f"  File Size: {metrics['file_size_mb']} MB")
        report.append(f"  Bitrate: {metrics['bitrate_kbps']} kbps")
        report.append("")
        
        if 'frame_quality' in metrics and 'error' not in metrics['frame_quality']:
            fq = metrics['frame_quality']
            report.append("Frame Quality:")
            report.append(f"  Brightness: {fq['avg_brightness']} ({fq['brightness_quality']})")
            report.append(f"  Contrast: {fq['avg_contrast']} ({fq['contrast_quality']})")
            report.append("")
        
        # Overall score
        score = metrics['quality_score']
        status = "✅ PASS" if metrics['passes_quality_check'] else "⚠️  NEEDS IMPROVEMENT"
        
        report.append(f"Quality Score: {score}/100 {status}")
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def batch_analyze(self, video_paths: list) -> Dict:
        """Analyze multiple videos and return summary"""
        results = []
        
        for path in video_paths:
            metrics = self.analyze_video(path)
            metrics['filename'] = os.path.basename(path)
            results.append(metrics)
        
        # Calculate averages
        valid_results = [r for r in results if 'error' not in r]
        
        if not valid_results:
            return {'error': 'No valid videos analyzed'}
        
        avg_score = np.mean([r['quality_score'] for r in valid_results])
        avg_duration = np.mean([r['duration'] for r in valid_results])
        pass_rate = (sum(1 for r in valid_results if r['passes_quality_check']) / len(valid_results)) * 100
        
        return {
            'total_analyzed': len(video_paths),
            'valid_videos': len(valid_results),
            'avg_quality_score': round(avg_score, 1),
            'avg_duration': round(avg_duration, 2),
            'pass_rate': round(pass_rate, 1),
            'results': results
        }


# Global instance
analyzer = QualityAnalyzer()


if __name__ == "__main__":
    print("Quality Analyzer Test")
    print("=" * 60)
    
    # Test with a video file
    test_video = "outputs/videos/test.mp4"
    
    if os.path.exists(test_video):
        print(analyzer.generate_quality_report(test_video))
    else:
        print("No test video found")
        print("\nQuality Thresholds:")
        for key, value in analyzer.quality_thresholds.items():
            print(f"  {key}: {value}")
