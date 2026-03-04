"""
REBUILT VIDEO EDITOR - Deterministic and Verifiable
No assumptions. Fail loudly. Runtime proof only.

Pipeline: Download → Normalize → Load → Validate → Trim → Merge → Export
"""

import os
import sys
import subprocess
import uuid
from typing import List, Optional
from moviepy import VideoFileClip, concatenate_videoclips
import imageio_ffmpeg

class VideoEditor:
    def __init__(self):
        self.output_dir = "outputs/videos"
        self.normalized_dir = "outputs/normalized"
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.normalized_dir, exist_ok=True)
        
        # Settings
        self.clip_duration = 3.0
        self.target_width = 640
        self.target_height = 360
        self.fps = 24
        self.min_clip_duration = 1.0
        
        # Get FFmpeg path
        try:
            self.ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
            print(f"[INIT] FFmpeg: {self.ffmpeg_path}")
        except Exception as e:
            raise RuntimeError(f"FFmpeg not available: {e}")
        
        print(f"[INIT] VideoEditor initialized")
        print(f"[INIT] Output: {self.output_dir}")
        print(f"[INIT] Normalized: {self.normalized_dir}")
    
    def normalize_video(self, input_path: str) -> str:
        """
        STEP 1: Normalize video with FFmpeg
        Returns: Path to normalized file
        Raises: Exception if normalization fails
        """
        print(f"\n[NORMALIZE] Input: {os.path.basename(input_path)}")
        
        # Verify input exists
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        input_size = os.path.getsize(input_path)
        print(f"[NORMALIZE] Input size: {input_size / 1024:.1f} KB")
        
        if input_size < 1000:
            raise ValueError(f"Input file too small: {input_size} bytes")
        
        # Generate output path
        basename = os.path.basename(input_path)
        name_without_ext = os.path.splitext(basename)[0]
        normalized_path = os.path.join(self.normalized_dir, f"norm_{name_without_ext}.mp4")
        
        # Skip if already normalized and valid
        if os.path.exists(normalized_path):
            existing_size = os.path.getsize(normalized_path)
            if existing_size > 1000:
                print(f"[NORMALIZE] Using cached: {existing_size / 1024:.1f} KB")
                return normalized_path
        
        # Run FFmpeg normalization
        print(f"[NORMALIZE] Running FFmpeg...")
        
        cmd = [
            self.ffmpeg_path,
            '-y',  # Overwrite
            '-i', input_path,
            '-vf', f'scale={self.target_width}:-2',  # Scale to target width
            '-r', str(self.fps),  # Set FPS
            '-an',  # No audio
            '-c:v', 'libx264',  # H.264 codec
            '-preset', 'fast',
            '-crf', '23',
            normalized_path
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                raise RuntimeError(f"FFmpeg failed: {result.stderr[-200:]}")
            
        except subprocess.TimeoutExpired:
            raise RuntimeError("FFmpeg timeout (60s)")
        
        # Verify output
        if not os.path.exists(normalized_path):
            raise RuntimeError("Normalized file not created")
        
        output_size = os.path.getsize(normalized_path)
        if output_size < 1000:
            os.remove(normalized_path)
            raise ValueError(f"Normalized file too small: {output_size} bytes")
        
        print(f"[NORMALIZE] Output size: {output_size / 1024:.1f} KB")
        print(f"[NORMALIZE] ✅ SUCCESS")
        
        return normalized_path
    
    def load_and_validate_clip(self, clip_path: str) -> VideoFileClip:
        """
        STEP 2: Load clip and validate
        Returns: Valid VideoFileClip
        Raises: Exception if invalid
        """
        print(f"\n[LOAD] Loading: {os.path.basename(clip_path)}")
        
        # Verify file exists
        if not os.path.exists(clip_path):
            raise FileNotFoundError(f"Clip not found: {clip_path}")
        
        # Load clip
        try:
            clip = VideoFileClip(clip_path)
        except Exception as e:
            raise RuntimeError(f"Failed to load clip: {e}")
        
        # Validate properties
        print(f"[LOAD] Resolution: {clip.w}x{clip.h}")
        print(f"[LOAD] FPS: {clip.fps}")
        print(f"[LOAD] Duration: {clip.duration:.2f}s")
        
        # Check duration
        if clip.duration is None:
            clip.close()
            raise ValueError("Duration is None")
        
        if clip.duration <= 0:
            clip.close()
            raise ValueError(f"Duration is {clip.duration} (must be > 0)")
        
        if clip.duration < self.min_clip_duration:
            clip.close()
            raise ValueError(f"Duration {clip.duration:.2f}s < minimum {self.min_clip_duration}s")
        
        print(f"[LOAD] ✅ VALID")
        
        return clip
    
    def trim_clip(self, clip: VideoFileClip) -> VideoFileClip:
        """
        STEP 3: Safely trim clip
        Returns: Trimmed clip
        Raises: Exception if trim fails
        """
        print(f"\n[TRIM] Original duration: {clip.duration:.2f}s")
        
        safe_duration = min(self.clip_duration, clip.duration)
        print(f"[TRIM] Target: {self.clip_duration:.2f}s")
        print(f"[TRIM] Safe trim to: {safe_duration:.2f}s")
        
        if safe_duration < clip.duration:
            try:
                clip = clip.subclipped(0, safe_duration)
                print(f"[TRIM] Trimmed to: {clip.duration:.2f}s")
            except Exception as e:
                raise RuntimeError(f"Trim failed: {e}")
        else:
            print(f"[TRIM] No trim needed")
        
        # Verify trimmed duration
        if clip.duration <= 0:
            raise ValueError(f"Trimmed duration is {clip.duration}")
        
        print(f"[TRIM] ✅ SUCCESS")
        
        return clip
    
    def process_clip(self, clip_path: str) -> Optional[VideoFileClip]:
        """
        Full clip processing pipeline
        Returns: Processed clip or None if failed
        """
        try:
            # Step 1: Normalize
            normalized_path = self.normalize_video(clip_path)
            
            # Step 2: Load and validate
            clip = self.load_and_validate_clip(normalized_path)
            
            # Step 3: Trim
            clip = self.trim_clip(clip)
            
            return clip
            
        except Exception as e:
            print(f"[PROCESS] ❌ FAILED: {e}")
            return None
    
    def create_video(
        self,
        clip_paths: List[str],
        prompt: str,
        output_filename: Optional[str] = None
    ) -> str:
        """
        Main video creation pipeline
        Returns: Path to output video
        Raises: Exception if creation fails
        """
        print("\n" + "=" * 60)
        print("VIDEO CREATION PIPELINE")
        print("=" * 60)
        print(f"Input clips: {len(clip_paths)}")
        print(f"Prompt: {prompt}")
        
        if not clip_paths:
            raise ValueError("No clip paths provided")
        
        # Process all clips
        print("\n[STAGE 1] Processing clips...")
        processed_clips = []
        
        for i, clip_path in enumerate(clip_paths):
            print(f"\n--- Clip {i+1}/{len(clip_paths)} ---")
            
            clip = self.process_clip(clip_path)
            
            if clip is not None:
                processed_clips.append(clip)
                print(f"[STAGE 1] Clip {i+1}: ✅ SUCCESS")
            else:
                print(f"[STAGE 1] Clip {i+1}: ❌ SKIPPED")
            
            # Limit to 3 clips
            if len(processed_clips) >= 3:
                print(f"[STAGE 1] Reached 3 clips limit")
                break
        
        # Verify we have clips
        if not processed_clips:
            raise RuntimeError("No valid clips after processing")
        
        print(f"\n[STAGE 1] Valid clips: {len(processed_clips)}")
        
        # Calculate expected duration
        total_duration = sum(c.duration for c in processed_clips)
        print(f"[STAGE 1] Expected total duration: {total_duration:.2f}s")
        
        # Concatenate
        print("\n[STAGE 2] Concatenating clips...")
        print(f"[STAGE 2] Method: compose")
        print(f"[STAGE 2] Clips: {len(processed_clips)}")
        
        try:
            final_video = concatenate_videoclips(processed_clips, method="compose")
            print(f"[STAGE 2] Concatenated duration: {final_video.duration:.2f}s")
            
            if final_video.duration <= 0:
                raise ValueError(f"Final video has 0 duration")
            
            print(f"[STAGE 2] ✅ SUCCESS")
            
        except Exception as e:
            # Close clips on error
            for clip in processed_clips:
                clip.close()
            raise RuntimeError(f"Concatenation failed: {e}")
        
        # Generate output path
        if not output_filename:
            video_id = str(uuid.uuid4())[:8]
            output_filename = f"video_{video_id}.mp4"
        
        output_path = os.path.join(self.output_dir, output_filename)
        
        # Export
        print("\n[STAGE 3] Exporting video...")
        print(f"[STAGE 3] Output: {output_path}")
        print(f"[STAGE 3] Codec: libx264")
        print(f"[STAGE 3] FPS: {self.fps}")
        print(f"[STAGE 3] Preset: medium")
        
        try:
            final_video.write_videofile(
                output_path,
                fps=self.fps,
                codec='libx264',
                preset='medium',
                audio=False,
                threads=4,
                logger=None
            )
            
            print(f"[STAGE 3] ✅ EXPORT COMPLETE")
            
        except Exception as e:
            # Close clips on error
            final_video.close()
            for clip in processed_clips:
                clip.close()
            raise RuntimeError(f"Export failed: {e}")
        
        # Close clips
        final_video.close()
        for clip in processed_clips:
            clip.close()
        
        print(f"[STAGE 3] Clips closed")
        
        # Verify output
        print("\n[STAGE 4] Verifying output...")
        
        if not os.path.exists(output_path):
            raise RuntimeError("Output file not created")
        
        output_size = os.path.getsize(output_path)
        print(f"[STAGE 4] File size: {output_size / 1024:.1f} KB")
        
        if output_size < 1000:
            raise ValueError(f"Output file too small: {output_size} bytes")
        
        # Reload and verify duration
        try:
            verify_clip = VideoFileClip(output_path)
            final_duration = verify_clip.duration
            verify_clip.close()
            
            print(f"[STAGE 4] Final duration: {final_duration:.2f}s")
            
            if final_duration <= 0:
                raise ValueError(f"Final duration is {final_duration}")
            
            print(f"[STAGE 4] ✅ VERIFIED")
            
        except Exception as e:
            raise RuntimeError(f"Output verification failed: {e}")
        
        # Success
        print("\n" + "=" * 60)
        print("✅ VIDEO CREATION SUCCESS")
        print("=" * 60)
        print(f"Output: {output_path}")
        print(f"Size: {output_size / 1024 / 1024:.2f} MB")
        print(f"Duration: {final_duration:.2f}s")
        print("=" * 60)
        
        return output_path


if __name__ == "__main__":
    print("VideoEditorRebuilt - Deterministic Video Processing")
    print("=" * 60)
    
    try:
        editor = VideoEditorRebuilt()
        print("\n✅ VideoEditor initialized successfully")
        print(f"Settings:")
        print(f"  Clip duration: {editor.clip_duration}s")
        print(f"  Resolution: {editor.target_width}x{editor.target_height}")
        print(f"  FPS: {editor.fps}")
        print(f"  Min duration: {editor.min_clip_duration}s")
        
    except Exception as e:
        print(f"\n❌ Initialization failed: {e}")
        sys.exit(1)
