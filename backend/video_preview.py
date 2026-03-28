"""
Video Preview Generator
Creates thumbnail previews and GIF previews from videos
"""

import os
from typing import Optional, List
from moviepy import VideoFileClip
from PIL import Image
import numpy as np

class VideoPreview:
    def __init__(self):
        self.preview_dir = "outputs/previews"
        os.makedirs(self.preview_dir, exist_ok=True)
    
    def generate_thumbnail(self, video_path: str, time_position: float = 0.5,
                          output_path: Optional[str] = None) -> str:
        """Generate thumbnail from video at specified time position (0.0-1.0)"""
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video not found: {video_path}")
        
        clip = VideoFileClip(video_path)
        
        # Calculate time position
        time_sec = clip.duration * time_position
        
        # Get frame
        frame = clip.get_frame(time_sec)
        
        # Generate output path
        if not output_path:
            base = os.path.splitext(os.path.basename(video_path))[0]
            output_path = os.path.join(self.preview_dir, f"{base}_thumb.jpg")
        
        # Save as image
        img = Image.fromarray(frame)
        img.save(output_path, quality=85)
        
        clip.close()
        
        print(f"✅ Thumbnail: {output_path}")
        return output_path
    
    def generate_gif_preview(self, video_path: str, duration: float = 3.0,
                            fps: int = 10, output_path: Optional[str] = None) -> str:
        """Generate GIF preview from video"""
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video not found: {video_path}")
        
        clip = VideoFileClip(video_path)
        
        # Limit duration
        preview_duration = min(duration, clip.duration)
        preview_clip = clip.subclipped(0, preview_duration)
        
        # Generate output path
        if not output_path:
            base = os.path.splitext(os.path.basename(video_path))[0]
            output_path = os.path.join(self.preview_dir, f"{base}_preview.gif")
        
        # Resize for smaller file
        preview_clip = preview_clip.resized(width=320)
        
        # Write GIF
        preview_clip.write_gif(output_path, fps=fps, program='ffmpeg')
        
        clip.close()
        preview_clip.close()
        
        file_size = os.path.getsize(output_path) / 1024
        print(f"✅ GIF Preview: {output_path} ({file_size:.1f}KB)")
        return output_path
    
    def generate_contact_sheet(self, video_path: str, grid_size: tuple = (3, 3),
                               output_path: Optional[str] = None) -> str:
        """Generate contact sheet with multiple frames"""
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video not found: {video_path}")
        
        clip = VideoFileClip(video_path)
        rows, cols = grid_size
        total_frames = rows * cols
        
        # Get frames at regular intervals
        times = np.linspace(0, clip.duration - 0.1, total_frames)
        frames = [clip.get_frame(t) for t in times]
        
        # Get frame dimensions
        frame_h, frame_w = frames[0].shape[:2]
        
        # Create contact sheet
        sheet_w = frame_w * cols
        sheet_h = frame_h * rows
        contact_sheet = np.zeros((sheet_h, sheet_w, 3), dtype=np.uint8)
        
        # Place frames
        for idx, frame in enumerate(frames):
            row = idx // cols
            col = idx % cols
            y = row * frame_h
            x = col * frame_w
            contact_sheet[y:y+frame_h, x:x+frame_w] = frame
        
        # Generate output path
        if not output_path:
            base = os.path.splitext(os.path.basename(video_path))[0]
            output_path = os.path.join(self.preview_dir, f"{base}_contact.jpg")
        
        # Save
        img = Image.fromarray(contact_sheet)
        img.save(output_path, quality=90)
        
        clip.close()
        
        print(f"✅ Contact Sheet: {output_path}")
        return output_path
    
    def generate_all_previews(self, video_path: str) -> dict:
        """Generate all preview types"""
        results = {}
        
        try:
            results['thumbnail'] = self.generate_thumbnail(video_path)
        except Exception as e:
            results['thumbnail_error'] = str(e)
        
        try:
            results['gif'] = self.generate_gif_preview(video_path)
        except Exception as e:
            results['gif_error'] = str(e)
        
        try:
            results['contact_sheet'] = self.generate_contact_sheet(video_path)
        except Exception as e:
            results['contact_sheet_error'] = str(e)
        
        return results


# Global instance
preview_generator = VideoPreview()


if __name__ == "__main__":
    print("Video Preview Generator Test")
    print("=" * 60)
    
    test_video = "outputs/videos/test.mp4"
    
    if os.path.exists(test_video):
        previews = preview_generator.generate_all_previews(test_video)
        print("\nGenerated Previews:")
        for key, value in previews.items():
            print(f"  {key}: {value}")
    else:
        print("No test video found")
