"""
Subtitle Generator
Generates and adds subtitles to videos
"""

import os
from typing import List, Dict, Optional
from datetime import timedelta

class Subtitle:
    """Represents a subtitle entry"""
    
    def __init__(self, index: int, start: float, end: float, text: str):
        self.index = index
        self.start = start
        self.end = end
        self.text = text
    
    def to_srt(self) -> str:
        """Convert to SRT format"""
        start_time = self._format_time(self.start)
        end_time = self._format_time(self.end)
        
        return f"{self.index}\n{start_time} --> {end_time}\n{self.text}\n"
    
    def _format_time(self, seconds: float) -> str:
        """Format time as HH:MM:SS,mmm"""
        td = timedelta(seconds=seconds)
        hours = td.seconds // 3600
        minutes = (td.seconds % 3600) // 60
        secs = td.seconds % 60
        millis = td.microseconds // 1000
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


class SubtitleGenerator:
    """Generates subtitles for videos"""
    
    def __init__(self, output_dir: str = "outputs/subtitles"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def create_subtitles(
        self,
        text_segments: List[Dict],
        output_filename: str
    ) -> str:
        """
        Create subtitle file from text segments
        
        Args:
            text_segments: List of {'start': float, 'end': float, 'text': str}
            output_filename: Output SRT filename
        
        Returns:
            Path to subtitle file
        """
        subtitles = []
        
        for i, segment in enumerate(text_segments, 1):
            subtitle = Subtitle(
                index=i,
                start=segment['start'],
                end=segment['end'],
                text=segment['text']
            )
            subtitles.append(subtitle)
        
        # Write to file
        output_path = os.path.join(self.output_dir, output_filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for subtitle in subtitles:
                f.write(subtitle.to_srt())
                f.write('\n')
        
        return output_path
    
    def generate_from_script(
        self,
        script: str,
        duration: float,
        words_per_segment: int = 5
    ) -> List[Dict]:
        """Generate subtitle segments from script"""
        words = script.split()
        segments = []
        
        # Calculate timing
        total_words = len(words)
        time_per_word = duration / total_words
        
        current_time = 0
        
        for i in range(0, len(words), words_per_segment):
            segment_words = words[i:i + words_per_segment]
            segment_text = ' '.join(segment_words)
            
            segment_duration = len(segment_words) * time_per_word
            
            segments.append({
                'start': current_time,
                'end': current_time + segment_duration,
                'text': segment_text
            })
            
            current_time += segment_duration
        
        return segments
    
    def add_subtitles_to_video(
        self,
        video_path: str,
        subtitle_path: str,
        output_path: Optional[str] = None
    ) -> str:
        """Add subtitles to video using FFmpeg"""
        import subprocess
        import imageio_ffmpeg
        
        if not output_path:
            output_path = video_path.replace('.mp4', '_subtitled.mp4')
        
        ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
        
        cmd = [
            ffmpeg_path,
            '-i', video_path,
            '-vf', f"subtitles={subtitle_path}",
            '-c:a', 'copy',
            output_path
        ]
        
        subprocess.run(cmd, check=True)
        
        return output_path
    
    def create_auto_subtitles(
        self,
        video_path: str,
        prompt: str,
        output_filename: Optional[str] = None
    ) -> str:
        """Create automatic subtitles based on prompt"""
        from moviepy import VideoFileClip
        
        # Get video duration
        clip = VideoFileClip(video_path)
        duration = clip.duration
        clip.close()
        
        # Generate segments
        segments = self.generate_from_script(prompt, duration)
        
        # Create subtitle file
        if not output_filename:
            video_basename = os.path.splitext(os.path.basename(video_path))[0]
            output_filename = f"{video_basename}.srt"
        
        return self.create_subtitles(segments, output_filename)


if __name__ == "__main__":
    generator = SubtitleGenerator()
    
    # Example usage
    segments = [
        {'start': 0.0, 'end': 3.0, 'text': 'Welcome to the video'},
        {'start': 3.0, 'end': 6.0, 'text': 'This is an example'},
        {'start': 6.0, 'end': 9.0, 'text': 'Of subtitle generation'}
    ]
    
    subtitle_path = generator.create_subtitles(segments, 'example.srt')
    print(f"✅ Subtitles created: {subtitle_path}")
