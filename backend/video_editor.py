"""
Optimized Video Editor - BULLETPROOF pipeline
FIXED: Proper duration handling, safe trimming, validation
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
        
        # Settings
        self.clip_duration = 3.0
        self.transition_duration = 0.3
        self.target_width = 640
        self.target_height = 360
        self.fps = 24
    
    def create_text_overlay(self, text: str, duration: float) -> CompositeVideoClip:
        """Create text overlay with fallback"""
        try:
            bg = ColorClip(
                size=(self.target_width, self.target_height), 
                color=(0, 0, 0), 
                duration=duration
            )
            
            txt = TextClip(
                text=text,
                font_size=40,
                color='white',
                text_align='center',
                size=(self.target_width - 40, None),
                method='caption'
            ).with_duration(duration).with_position('center')
            
            video = CompositeVideoClip([bg, txt])
            return video
            
        except Exception as e:
            print(f"⚠️  Text overlay error: {e}, using black screen")
            return ColorClip(
                size=(self.target_width, self.target_height), 
                color=(0, 0, 0), 
                duration=duration
            )
    
    def process_clip(self, clip_path: str) -> Optional[VideoFileClip]:
        """
        ✅ BULLETPROOF clip processing
        - Validates file exists
        - Checks duration > 0
        - Safe trimming with min()
        - Proper error handling
        """
        try:
            # ✅ VERIFY FILE EXISTS
            if not os.path.exists(clip_path):
                print(f"❌ File not found: {clip_path}")
                return None
            
            # ✅ VERIFY FILE SIZE
            file_size = os.path.getsize(clip_path)
            if file_size < 1000:
                print(f"❌ File too small ({file_size} bytes): {clip_path}")
                return None
            
            print(f"⚡ Loading: {os.path.basename(clip_path)} ({file_size / 1024:.1f}KB)")
            
            # ✅ LOAD CLIP
            clip = VideoFileClip(clip_path)
            
            # ✅ DEBUG: Print duration
            print(f"   Duration: {clip.duration:.2f}s")
            
            # ✅ VALIDATE DURATION > 0
            if clip.duration <= 0:
                print(f"❌ Clip has 0 duration, skipping")
                clip.close()
                return None
            
            # ✅ VALIDATE MINIMUM DURATION
            if clip.duration < 0.5:
                print(f"⚠️  Clip too short ({clip.duration:.2f}s), skipping")
                clip.close()
                return None
            
            # ✅ SAFE TRIMMING: Use min() to prevent errors
            trim_duration = min(self.clip_duration, clip.duration)
            print(f"   Trimming to: {trim_duration:.2f}s")
            
            if trim_duration < clip.duration:
                clip = clip.subclipped(0, trim_duration)
            
            # ✅ VERIFY TRIMMED DURATION
            if clip.duration <= 0:
                print(f"❌ Clip became 0 duration after trim")
                clip.close()
                return None
            
            # Resize to target resolution
            clip = clip.resized(height=self.target_height)
            
            if clip.w != self.target_width:
                clip = clip.resized(width=self.target_width)
            
            # Add transitions
            clip = clip.with_effects([
                vfx.FadeIn(self.transition_duration),
                vfx.FadeOut(self.transition_duration)
            ])
            
            print(f"✅ Processed: {os.path.basename(clip_path)} - {clip.duration:.2f}s")
            return clip
            
        except Exception as e:
            print(f"❌ Error processing {clip_path}: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def create_video(
        self, 
        clip_paths: List[str], 
        prompt: str,
        output_filename: Optional[str] = None
    ) -> Optional[str]:
        """
        ✅ BULLETPROOF video creation
        - Validates all clips
        - Never concatenates empty list
        - Proper error handling
        - Debug output
        """
        
        if not clip_paths:
            print("❌ No clips provided")
            return None
        
        try:
            print("\n🎬 Creating video with bulletproof pipeline...")
            print(f"📋 Input clips: {len(clip_paths)}")
            
            # ✅ PROCESS AND VALIDATE ALL CLIPS
            processed_clips = []
            for i, clip_path in enumerate(clip_paths):
                print(f"\n📹 Processing clip {i+1}/{len(clip_paths)}")
                
                clip = self.process_clip(clip_path)
                if clip and clip.duration > 0:
                    processed_clips.append(clip)
                else:
                    print(f"⚠️  Skipping invalid clip: {clip_path}")
                
                # Limit to 3 clips
                if len(processed_clips) >= 3:
                    break
            
            # ✅ VALIDATE WE HAVE CLIPS
            if not processed_clips:
                print("❌ No valid clips to process")
                raise ValueError("No valid clips available for video creation")
            
            print(f"\n✅ Valid clips: {len(processed_clips)}")
            for i, clip in enumerate(processed_clips):
                print(f"   Clip {i+1}: {clip.duration:.2f}s")
            
            # Create intro text
            print("\n📝 Creating text overlay...")
            intro_text = self.create_text_overlay(
                f'"{prompt}"',
                duration=1.5
            )
            print(f"   Text duration: {intro_text.duration:.2f}s")
            
            # ✅ COMBINE CLIPS (NEVER EMPTY LIST)
            print("\n🔗 Combining clips...")
            all_clips = [intro_text] + processed_clips
            
            print(f"   Total clips to combine: {len(all_clips)}")
            total_duration = sum(c.duration for c in all_clips)
            print(f"   Expected total duration: {total_duration:.2f}s")
            
            final_video = concatenate_videoclips(
                all_clips, 
                method="compose"
            )
            
            # ✅ VALIDATE FINAL VIDEO
            if final_video.duration <= 0:
                print("❌ Final video has 0 duration!")
                raise ValueError("Final video duration is 0")
            
            print(f"✅ Final video duration: {final_video.duration:.2f}s")
            
            # Generate output filename
            if not output_filename:
                video_id = str(uuid.uuid4())[:8]
                output_filename = f"video_{video_id}.mp4"
            
            output_path = os.path.join(self.output_dir, output_filename)
            
            # ✅ EXPORT WITH PROPER SETTINGS
            print(f"\n💾 Exporting to: {output_path}")
            final_video.write_videofile(
                output_path,
                fps=self.fps,
                codec='libx264',  # ✅ EXPLICIT CODEC
                audio=False,
                preset='ultrafast',
                threads=4,
                bitrate='500k',
                logger=None
            )
            
            # ✅ VERIFY OUTPUT FILE
            if not os.path.exists(output_path):
                print("❌ Output file was not created!")
                raise ValueError("Video export failed - file not created")
            
            file_size = os.path.getsize(output_path)
            if file_size < 1000:
                print(f"❌ Output file too small ({file_size} bytes)")
                raise ValueError("Video export failed - file too small")
            
            print(f"✅ Video created successfully!")
            print(f"   Path: {output_path}")
            print(f"   Size: {file_size / 1024 / 1024:.2f}MB")
            print(f"   Duration: {final_video.duration:.2f}s")
            
            # Cleanup
            final_video.close()
            for clip in processed_clips:
                clip.close()
            intro_text.close()
            
            return output_path
            
        except Exception as e:
            print(f"\n❌ CRITICAL ERROR in video creation: {e}")
            import traceback
            traceback.print_exc()
            return None


if __name__ == "__main__":
    # Test
    editor = VideoEditor()
    print("✅ Video Editor initialized")
    print(f"   Resolution: {editor.target_width}x{editor.target_height}")
    print(f"   Clip duration: {editor.clip_duration}s")
    print(f"   FPS: {editor.fps}")
