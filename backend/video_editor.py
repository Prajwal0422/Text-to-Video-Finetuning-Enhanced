"""
Video Editor - Combines clips, adds transitions and text overlays
"""

import os
from typing import List, Optional
from moviepy import (
    VideoFileClip, 
    concatenate_videoclips, 
    TextClip, 
    CompositeVideoClip,
    ColorClip,
    vfx
)
import uuid

class VideoEditor:
    def __init__(self):
        self.output_dir = "outputs/videos"
        os.makedirs(self.output_dir, exist_ok=True)
        self.default_duration = 3.0  # seconds per clip
        self.transition_duration = 0.5  # crossfade duration
    
    def create_text_overlay(self, text: str, duration: float, size: tuple = (1280, 720)) -> CompositeVideoClip:
        """Create a text overlay clip"""
        try:
            # Create background
            bg = ColorClip(size=size, color=(0, 0, 0), duration=duration)
            
            # Create text
            txt = TextClip(
                text,
                fontsize=50,
                color='white',
                font='Arial',
                size=(size[0] - 100, None),
                method='caption',
                align='center'
            ).set_duration(duration).set_position('center')
            
            # Composite
            video = CompositeVideoClip([bg, txt])
            return video
            
        except Exception as e:
            print(f"⚠️  Error creating text overlay: {e}")
            # Return black clip as fallback
            return ColorClip(size=size, color=(0, 0, 0), duration=duration)
    
    def process_clip(self, clip_path: str, target_duration: float) -> Optional[VideoFileClip]:
        """Load and process a single clip"""
        try:
            clip = VideoFileClip(clip_path)
            
            # Trim to target duration
            if clip.duration > target_duration:
                clip = clip.subclip(0, target_duration)
            
            # Resize to standard resolution
            clip = clip.resized(height=720)
            
            # Add fade effects
            clip = clip.with_effects([vfx.FadeIn(self.transition_duration), vfx.FadeOut(self.transition_duration)])
            
            return clip
            
        except Exception as e:
            print(f"❌ Error processing clip {clip_path}: {e}")
            return None
    
    def create_video(
        self, 
        clip_paths: List[str], 
        prompt: str,
        output_filename: Optional[str] = None
    ) -> Optional[str]:
        """Main method to create final video"""
        
        if not clip_paths:
            print("❌ No clips provided")
            return None
        
        try:
            print("🎬 Starting video creation...")
            
            # Process all clips
            processed_clips = []
            for i, clip_path in enumerate(clip_paths):
                print(f"📹 Processing clip {i+1}/{len(clip_paths)}")
                
                if os.path.exists(clip_path):
                    clip = self.process_clip(clip_path, self.default_duration)
                    if clip:
                        processed_clips.append(clip)
            
            if not processed_clips:
                print("❌ No valid clips to process")
                return None
            
            # Add intro text overlay
            print("📝 Adding text overlay...")
            intro_text = self.create_text_overlay(
                f'"{prompt}"',
                duration=2.0
            )
            
            # Combine all clips
            print("🔗 Combining clips...")
            all_clips = [intro_text] + processed_clips
            final_video = concatenate_videoclips(all_clips, method="compose")
            
            # Generate output filename
            if not output_filename:
                video_id = str(uuid.uuid4())[:8]
                output_filename = f"video_{video_id}.mp4"
            
            output_path = os.path.join(self.output_dir, output_filename)
            
            # Export video
            print("💾 Exporting video...")
            final_video.write_videofile(
                output_path,
                fps=24,
                codec='libx264',
                audio=False,
                preset='ultrafast',
                threads=4,
                logger=None  # Suppress moviepy logs
            )
            
            # Cleanup
            final_video.close()
            for clip in processed_clips:
                clip.close()
            
            print(f"✅ Video created: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ Error creating video: {e}")
            return None


if __name__ == "__main__":
    # Test
    editor = VideoEditor()
    
    # Create a simple test video with text
    test_prompt = "Test video generation"
    output = editor.create_video([], test_prompt)
    
    if output:
        print(f"Test video created: {output}")
