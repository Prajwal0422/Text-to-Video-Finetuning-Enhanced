"""
PHASE 3: SINGLE CLIP EXPORT TEST
Load, validate, trim, and export a single clip
"""

import os
import sys
from moviepy import VideoFileClip

def test_single_clip_export():
    print("=" * 60)
    print("PHASE 3: SINGLE CLIP EXPORT TEST")
    print("=" * 60)
    
    # Input file (from Phase 2)
    input_path = "outputs/test_clips/normalized_test_clip.mp4"
    output_path = "outputs/test_clips/single_test_output.mp4"
    
    # Verify input exists
    print("\n[STEP 1] Verifying input file")
    
    if not os.path.exists(input_path):
        print(f"❌ ABORT: Input file not found: {input_path}")
        print("Run test_download_and_normalize.py first")
        sys.exit(1)
    
    input_size = os.path.getsize(input_path)
    print(f"Input file: {input_path}")
    print(f"Input size: {input_size / 1024:.1f} KB")
    print("✅ PASS")
    
    # Load clip
    print("\n[STEP 2] Loading clip with MoviePy")
    
    try:
        clip = VideoFileClip(input_path)
        print(f"Clip loaded successfully")
        print(f"Resolution: {clip.w}x{clip.h}")
        print(f"FPS: {clip.fps}")
        print(f"Duration: {clip.duration} seconds")
        
    except Exception as e:
        print(f"❌ ABORT: Failed to load clip")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Validate duration
    print("\n[STEP 3] Validating duration")
    
    if clip.duration is None:
        print(f"❌ ABORT: Duration is None")
        clip.close()
        sys.exit(1)
    
    if clip.duration <= 0:
        print(f"❌ ABORT: Duration is {clip.duration} (must be > 0)")
        clip.close()
        sys.exit(1)
    
    print(f"Duration: {clip.duration:.2f}s")
    print("✅ PASS: Duration valid")
    
    # Safe trimming
    print("\n[STEP 4] Trimming clip safely")
    
    target_duration = 3.0
    safe_duration = min(target_duration, clip.duration)
    
    print(f"Target duration: {target_duration}s")
    print(f"Actual duration: {clip.duration:.2f}s")
    print(f"Safe trim to: {safe_duration:.2f}s")
    
    if safe_duration < clip.duration:
        try:
            clip = clip.subclipped(0, safe_duration)
            print(f"Trimmed to: {clip.duration:.2f}s")
        except Exception as e:
            print(f"❌ ABORT: Trim failed")
            print(f"Error: {e}")
            clip.close()
            sys.exit(1)
    else:
        print("No trim needed (clip shorter than target)")
    
    print("✅ PASS: Trim successful")
    
    # Export
    print("\n[STEP 5] Exporting video")
    
    # Remove old output
    if os.path.exists(output_path):
        os.remove(output_path)
        print(f"Removed old output: {output_path}")
    
    print(f"Output path: {output_path}")
    print("Export settings:")
    print("  codec: libx264")
    print("  fps: 24")
    print("  preset: medium")
    print("  audio: False")
    print("  threads: 4")
    
    try:
        clip.write_videofile(
            output_path,
            codec='libx264',
            fps=24,
            preset='medium',
            audio=False,
            threads=4,
            logger=None  # Suppress MoviePy progress bar
        )
        
        print("Export completed")
        
    except Exception as e:
        print(f"❌ ABORT: Export failed")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        clip.close()
        sys.exit(1)
    
    # Close clip
    clip.close()
    print("Clip closed")
    
    # Verify output
    print("\n[STEP 6] Verifying output file")
    
    if not os.path.exists(output_path):
        print(f"❌ ABORT: Output file not created")
        sys.exit(1)
    
    output_size = os.path.getsize(output_path)
    print(f"Output size: {output_size / 1024:.1f} KB")
    
    if output_size < 10 * 1024:  # 10KB minimum
        print(f"❌ ABORT: Output file too small (< 10KB)")
        sys.exit(1)
    
    print("✅ PASS: Output file valid")
    
    # Reload and verify duration
    print("\n[STEP 7] Reloading to verify duration")
    
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
    print("✅ PHASE 3 COMPLETE: SINGLE CLIP EXPORTED")
    print("=" * 60)
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
        output_path = test_single_clip_export()
        print(f"\n✅ SUCCESS: {output_path}")
    except KeyboardInterrupt:
        print("\n❌ ABORTED BY USER")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
