"""
Optimized Video Editor - Fast processing with immediate trimming
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
        
        # OPTIMIZED SETTINGS
        self.clip_duration = 3.0  # Only 3 seconds per clip
        self.transition_duration = 0.3  # Shorter transitions (0.3s)
        self.target_width = 640  # Small resolution for speed
        self.target_height = 360  # 640x360 (16:9)
        self.fps = 24  # Standard FPS
    
    def create_text_overlay(self, text: str, duration: float) -> CompositeVideoClip:
        """Create a simple text overlay (optimized)"""
        try:
            # Create black background
            bg = ColorClip(
                size=(self.target_width, self.target_height), 
                color=(0, 0, 0), 
                duration=duration
            )
            
            # Create text (simplified for speed)
            txt = TextClip(
                text=text,
                font_size=40,
                color='white',
                font='Arial',
                text_align='center',
                size=(self.target_width - 40, None),
                method='caption'
            ).with_duration(duration).with_position('center')
            
            # Composite
            video = CompositeVideoClip([bg, txt])
            return video
            
        except Exception as e:
            print(f"⚠️  Text overlay error: {e}")
            # Fallback: black clip
            return ColorClip(
                size=(self.target_width, self.target_height), 
                color=(0, 0, 0), 
                duration=duration
            )
    
    def process_clip(self, clip_path: str) -> Optional[VideoFileClip]:
        """
        Load and process clip with IMMEDIATE TRIMMING
        - Trim to 3 seconds immediately
        - Resize to small resolution
        - Add quick transitions
        """
        try:
            print(f"⚡ Processing: {os.path.basename(clip_path)}")
            
            # Load clip
            clip = VideoFileClip(clip_path)
            
            # IMMEDIATE TRIM: Only use first 3 seconds
            if clip.duration > self.clip_duration:
                clip = clip.subclipped(0, self.clip_duration)
            
            # Resize to small resolution (SPEED OPTIMIZATION)
            clip = clip.resized(height=self.target_height)
            
            # Ensure correct dimensions
            if clip.w != self.target_width:
                clip = clip.resized(width=self.target_width)
            
            # Add quick fade effects
            clip = clip.with_effects([
                vfx.FadeIn(self.transition_duration),
                vfx.FadeOut(self.transition_duration)
            ])
            
            return clip
            
        except Exception as e:
            print(f"❌ Error processing {clip_path}: {e}")
            return None
    
    def create_video(
        self, 
        clip_paths: List[str], 
        prompt: str,
        output_filename: Optional[str] = None
    ) -> Optional[str]:
        """
        Create video with OPTIMIZED settings:
        - Small resolution (640x360)
        - Fast encoding (ultrafast preset)
        - Minimal processing
        - Quick export
        """
        
        if not clip_paths:
            print("❌ No clips provided")
            return None
        
        try:
            print("\n🎬 Creating optimized video...")
            
            # Process clips in parallel-ready way (though moviepy is sequential)
            processed_clips = []
            for i, clip_path in enumerate(clip_paths):
                if not os.path.exists(clip_path):
                    print(f"⚠️  Clip not found: {clip_path}")
                    continue
                
                clip = self.process_clip(clip_path)
                if clip:
                    processed_clips.append(clip)
                    
                # LIMIT: Stop at 3 clips max
                if len(processed_clips) >= 3:
                    break
            
            if not processed_clips:
                print("❌ No valid clips to process")
                return None
            
            print(f"✅ Processed {len(processed_clips)} clips")
            
            # Create intro text (short - 1.5s only)
            print("📝 Adding text overlay...")
            intro_text = self.create_text_overlay(
                f'"{prompt}"',
                duration=1.5  # Shorter intro
            )
            
            # Combine clips
            print("🔗 Combining clips...")
            all_clips = [intro_text] + processed_clips
            
            final_video = concatenate_videoclips(
                all_clips, 
                method="compose"
            )
            
            # Generate output filename
            if not output_filename:
                video_id = str(uuid.uuid4())[:8]
                output_filename = f"video_{video_id}.mp4"
            
            output_path = os.path.join(self.output_dir, output_filename)
            
            # OPTIMIZED EXPORT SETTINGS
            print("💾 Exporting video (optimized)...")
            final_video.write_videofile(
                output_path,
                fps=self.fps,
                codec='libx264',
                audio=False,  # No audio for speed
                preset='ultrafast',  # Fastest encoding
                threads=4,
                bitrate='500k',  # Lower bitrate for speed
                logger=None,  # Suppress logs
                verbose=False
            )
            
            # Cleanup
            final_video.close()
            for clip in processed_clips:
                clip.close()
            intro_text.close()
            
            # Get file size
            file_size = os.path.getsize(output_path) / 1024 / 1024
            print(f"✅ Video created: {output_path} ({file_size:.1f}MB)")
            
            return output_path
            
        except Exception as e:
            print(f"❌ Error creating video: {e}")
            import traceback
            traceback.print_exc()
            return None


if __name__ == "__main__":
    # Test optimized editor
    editor = VideoEditor()
    print("Video Editor initialized")
    print(f"Target resolution: {editor.target_width}x{editor.target_height}")
    print(f"Clip duration: {editor.clip_duration}s")
    print(f"FPS: {editor.fps}")
