"""
PHASE 4: MULTI-CLIP MERGE TEST
Load multiple clips, validate, and concatenate
"""

import os
import sys
import subprocess
import imageio_ffmpeg
from moviepy import VideoFileClip, concatenate_videoclips

def create_test_clips():
    """Create 2-3 test clips by duplicating the normalized clip"""
    print("\n[SETUP] Creating test clips")
    
    source = "outputs/test_clips/normalized_test_clip.mp4"
    output_dir = "outputs/test_clips"
    
    if not os.path.exists(source):
        print(f"❌ ABORT: Source clip not found: {source}")
        print("Run test_download_and_normalize.py first")
        sys.exit(1)
    
    # Create 3 copies with different names
    test_clips = []
    for i in range(1, 4):
        dest = os.path.join(output_dir, f"test_clip_{i}.mp4")
        
        # Copy using ffmpeg (fast)
        if not os.path.exists(dest):
            ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
            cmd = [ffmpeg_path, '-y', '-i', source, '-c', 'copy', dest]
            
            result = subprocess.run(cmd, capture_output=True, timeout=30)
            if result.returncode != 0:
                print(f"❌ ABORT: Failed to create {dest}")
                sys.exit(1)
            
            print(f"Created: {dest}")
        else:
            print(f"Using existing: {dest}")
        
        test_clips.append(dest)
    
    return test_clips

def test_multi_clip_merge():
    print("=" * 60)
    print("PHASE 4: MULTI-CLIP MERGE TEST")
    print("=" * 60)
    
    # Create test clips
    clip_paths = create_test_clips()
    output_path = "outputs/test_clips/multi_test_output.mp4"
    
    # Load and validate clips
    print("\n[STEP 1] Loading and validating clips")
    
    loaded_clips = []
    total_expected_duration = 0
    
    for i, path in enumerate(clip_paths):
        print(f"\nClip {i+1}: {os.path.basename(path)}")
        
        # Verify file exists
        if not os.path.exists(path):
            print(f"❌ ABORT: File not found: {path}")
            sys.exit(1)
        
        file_size = os.path.getsize(path)
        print(f"  Size: {file_size / 1024:.1f} KB")
        
        # Load clip
        try:
            clip = VideoFileClip(path)
            print(f"  Resolution: {clip.w}x{clip.h}")
            print(f"  FPS: {clip.fps}")
            print(f"  Duration: {clip.duration:.2f}s")
            
        except Exception as e:
            print(f"❌ ABORT: Failed to load clip {i+1}")
            print(f"Error: {e}")
            # Close any loaded clips
            for c in loaded_clips:
                c.close()
            sys.exit(1)
        
        # Validate duration
        if clip.duration is None or clip.duration <= 0:
            print(f"❌ ABORT: Invalid duration: {clip.duration}")
            clip.close()
            for c in loaded_clips:
                c.close()
            sys.exit(1)
        
        # Check minimum duration
        if clip.duration < 1.0:
            print(f"❌ ABORT: Duration too short (< 1s): {clip.duration:.2f}s")
            clip.close()
            for c in loaded_clips:
                c.close()
            sys.exit(1)
        
        print(f"  ✅ Valid")
        
        loaded_clips.append(clip)
        total_expected_duration += clip.duration
    
    print(f"\n✅ PASS: All {len(loaded_clips)} clips loaded and validated")
    print(f"Expected total duration: {total_expected_duration:.2f}s")
    
    # Concatenate
    print("\n[STEP 2] Concatenating clips")
    print(f"Method: compose")
    print(f"Clips to merge: {len(loaded_clips)}")
    
    try:
        final_clip = concatenate_videoclips(loaded_clips, method="compose")
        print(f"Concatenation successful")
        print(f"Final duration: {final_clip.duration:.2f}s")
        
        # Verify duration
        if final_clip.duration <= 0:
            print(f"❌ ABORT: Final clip has 0 duration")
            final_clip.close()
            for c in loaded_clips:
                c.close()
            sys.exit(1)
        
        # Check if duration matches expected
        duration_diff = abs(final_clip.duration - total_expected_duration)
        if duration_diff > 0.5:  # Allow 0.5s tolerance
            print(f"⚠️  WARNING: Duration mismatch")
            print(f"  Expected: {total_expected_duration:.2f}s")
            print(f"  Actual: {final_clip.duration:.2f}s")
            print(f"  Difference: {duration_diff:.2f}s")
        
        print("✅ PASS: Concatenation successful")
        
    except Exception as e:
        print(f"❌ ABORT: Concatenation failed")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        for c in loaded_clips:
            c.close()
        sys.exit(1)
    
    # Export
    print("\n[STEP 3] Exporting merged video")
    
    # Remove old output
    if os.path.exists(output_path):
        os.remove(output_path)
        print(f"Removed old output")
    
    print(f"Output: {output_path}")
    print("Export settings:")
    print("  codec: libx264")
    print("  fps: 24")
    print("  preset: medium")
    print("  audio: False")
    print("  threads: 4")
    
    try:
        final_clip.write_videofile(
            output_path,
            codec='libx264',
            fps=24,
            preset='medium',
            audio=False,
            threads=4,
            logger=None
        )
        
        print("Export completed")
        
    except Exception as e:
        print(f"❌ ABORT: Export failed")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        final_clip.close()
        for c in loaded_clips:
            c.close()
        sys.exit(1)
    
    # Close clips
    final_clip.close()
    for clip in loaded_clips:
        clip.close()
    print("All clips closed")
    
    # Verify output
    print("\n[STEP 4] Verifying output file")
    
    if not os.path.exists(output_path):
        print(f"❌ ABORT: Output file not created")
        sys.exit(1)
    
    output_size = os.path.getsize(output_path)
    print(f"Output size: {output_size / 1024:.1f} KB")
    
    if output_size < 100 * 1024:  # 100KB minimum
        print(f"❌ ABORT: Output file too small (< 100KB)")
        sys.exit(1)
    
    print("✅ PASS: Output file size valid")
    
    # Reload and verify
    print("\n[STEP 5] Reloading to verify")
    
    try:
        verify_clip = VideoFileClip(output_path)
        final_duration = verify_clip.duration
        verify_clip.close()
        
        print(f"Final duration: {final_duration:.2f}s")
        
        if final_duration <= 0:
            print(f"❌ ABORT: Final duration is {final_duration}")
            sys.exit(1)
        
        print("✅ PASS: Final duration valid")
        
    except Exception as e:
        print(f"❌ ABORT: Failed to reload output")
        print(f"Error: {e}")
        sys.exit(1)
    
    # Final summary
    print("\n" + "=" * 60)
    print("✅ PHASE 4 COMPLETE: MULTI-CLIP MERGED")
    print("=" * 60)
    print(f"Input clips: {len(clip_paths)}")
    print(f"Output: {output_path}")
    print(f"Size: {output_size / 1024:.1f} KB")
    print(f"Duration: {final_duration:.2f}s")
    print("=" * 60)
    print("\nTest playback:")
    print(f"  VLC: vlc {output_path}")
    print(f"  Browser: file://{os.path.abspath(output_path)}")
    print("=" * 60)
    
    return output_path

if __name__ == "__main__":
    try:
        output_path = test_multi_clip_merge()
        print(f"\n✅ SUCCESS: {output_path}")
    except KeyboardInterrupt:
        print("\n❌ ABORTED BY USER")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
