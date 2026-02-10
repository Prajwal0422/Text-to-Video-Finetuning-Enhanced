"""
SAFE VIDEO PIPELINE - Zero-second video bug ELIMINATED
Implements all mandatory safety rules
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
        self.min_clip_duration = 0.5  # RULE 2: Skip clips shorter than 0.5s
    
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
        SAFE CLIP PROCESSING
        Implements RULE 1, 2, 3
        """
        try:
            # Verify file exists
            if not os.path.exists(clip_path):
                print(f"❌ File not found: {clip_path}")
                return None
            
            # Verify file size
            file_size = os.path.getsize(clip_path)
            if file_size < 1000:
                print(f"❌ File too small ({file_size} bytes): {clip_path}")
                return None
            
            print(f"⚡ Loading: {os.path.basename(clip_path)} ({file_size / 1024:.1f}KB)")
            
            # Load clip
            clip = VideoFileClip(clip_path)
            
            # RULE 1: PRINT DURATION BEFORE USE
            print(f"   📊 Original duration: {clip.duration:.2f}s")
            
            # RULE 2: SKIP CLIPS SHORTER THAN 0.5 SECONDS
            if clip.duration < self.min_clip_duration:
                print(f"❌ Skipping too short clip ({clip.duration:.2f}s < {self.min_clip_duration}s)")
                clip.close()
                return None
            
            # RULE 3: TRIM USING min(clip.duration, 3)
            safe_end = min(self.clip_duration, clip.duration)
            print(f"   ✂️  Trimming to: {safe_end:.2f}s")
            
            if safe_end < clip.duration:
                clip = clip.subclipped(0, safe_end)
            
            # Verify trimmed duration
            print(f"   ✅ Trimmed duration: {clip.duration:.2f}s")
            
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
            
            print(f"✅ Processed successfully: {clip.duration:.2f}s")
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
        SAFE VIDEO CREATION PIPELINE
        Implements ALL MANDATORY RULES
        """
        
        if not clip_paths:
            print("❌ No clips provided")
            return None
        
        try:
            print("\n" + "="*60)
            print("🎬 SAFE VIDEO PIPELINE - Starting")
            print("="*60)
            print(f"📋 Input clips: {len(clip_paths)}")
            
            # Process all clips
            processed_clips = []
            for i, clip_path in enumerate(clip_paths):
                print(f"\n📹 Processing clip {i+1}/{len(clip_paths)}")
                
                clip = self.process_clip(clip_path)
                if clip and clip.duration > 0:
                    processed_clips.append(clip)
                else:
                    print(f"⚠️  Skipping invalid clip")
                
                # Limit to 3 clips
                if len(processed_clips) >= 3:
                    break
            
            # RULE 7: RAISE ERROR IF NO VALID CLIPS
            if not processed_clips:
                print("\n❌ CRITICAL: No valid clips available")
                raise ValueError("All clips are invalid - cannot create video")
            
            print(f"\n✅ Valid clips collected: {len(processed_clips)}")
            
            # STEP 1: VERIFY CLIPS (MOST IMPORTANT)
            print("\n" + "-"*60)
            print("---- CLIP DEBUG ----")
            for i, c in enumerate(processed_clips):
                print(f"Clip {i} duration: {c.duration:.2f}s")
            print("-"*60)
            
            # STEP 3: SAFE CONCATENATION
            # Filter clips > 0.5s
            valid_clips = [c for c in processed_clips if c.duration > self.min_clip_duration]
            
            if len(valid_clips) == 0:
                print("❌ All clips too short after filtering")
                raise Exception("All clips invalid!")
            
            print(f"\n✅ Clips after filtering: {len(valid_clips)}")
            
            # Create intro text
            print("\n📝 Creating text overlay...")
            intro_text = self.create_text_overlay(
                f'"{prompt}"',
                duration=1.5
            )
            print(f"   Text duration: {intro_text.duration:.2f}s")
            
            # Combine clips
            print("\n🔗 Combining clips...")
            all_clips = [intro_text] + valid_clips
            
            print(f"   Total clips to combine: {len(all_clips)}")
            total_duration = sum(c.duration for c in all_clips)
            print(f"   Expected total duration: {total_duration:.2f}s")
            
            # RULE 4: USE method="compose"
            print("\n🎬 Concatenating with method='compose'...")
            final_video = concatenate_videoclips(
                all_clips, 
                method="compose"  # MANDATORY
            )
            
            # Validate final video
            print(f"✅ Final video duration: {final_video.duration:.2f}s")
            
            if final_video.duration <= 0:
                print("❌ Final video has 0 duration!")
                raise ValueError("Final video duration is 0")
            
            # Generate output filename
            if not output_filename:
                video_id = str(uuid.uuid4())[:8]
                output_filename = f"video_{video_id}.mp4"
            
            output_path = os.path.join(self.output_dir, output_filename)
            
            # RULE 6: EXPORT WITH CORRECT SETTINGS
            print(f"\n💾 Exporting to: {output_path}")
            print("   Settings:")
            print(f"   - codec: libx264")
            print(f"   - fps: {self.fps}")
            print(f"   - preset: medium")
            print(f"   - threads: 4")
            print(f"   - audio: False")
            
            final_video.write_videofile(
                output_path,
                fps=self.fps,           # RULE 6
                codec='libx264',        # RULE 6
                preset='medium',        # RULE 6
                audio=False,            # RULE 6
                threads=4,              # RULE 6
                logger=None
            )
            
            # Verify output file
            if not os.path.exists(output_path):
                print("❌ Output file was not created!")
                raise ValueError("Video export failed - file not created")
            
            file_size = os.path.getsize(output_path)
            if file_size < 1000:
                print(f"❌ Output file too small ({file_size} bytes)")
                raise ValueError("Video export failed - file too small")
            
            print("\n" + "="*60)
            print("✅ VIDEO CREATED SUCCESSFULLY!")
            print("="*60)
            print(f"   Path: {output_path}")
            print(f"   Size: {file_size / 1024 / 1024:.2f}MB")
            print(f"   Duration: {final_video.duration:.2f}s")
            print("="*60 + "\n")
            
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
    print("✅ SAFE VIDEO PIPELINE initialized")
    print(f"   Resolution: {editor.target_width}x{editor.target_height}")
    print(f"   Clip duration: {editor.clip_duration}s")
    print(f"   Min clip duration: {editor.min_clip_duration}s")
    print(f"   FPS: {editor.fps}")
