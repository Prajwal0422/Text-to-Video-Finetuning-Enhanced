"""
PHASE 6: FINAL INTEGRATION TEST
Complete end-to-end pipeline test with timing
"""

import os
import sys
import time
from video_editor_rebuilt import VideoEditorRebuilt

def final_pipeline_test():
    print("=" * 60)
    print("PHASE 6: FINAL INTEGRATION TEST")
    print("=" * 60)
    
    # Use test clips from previous phases
    test_clips = [
        "outputs/test_clips/test_clip_1.mp4",
        "outputs/test_clips/test_clip_2.mp4",
        "outputs/test_clips/test_clip_3.mp4"
    ]
    
    # Verify test clips exist
    print("\n[SETUP] Verifying test clips...")
    
    existing_clips = []
    for clip_path in test_clips:
        if os.path.exists(clip_path):
            size = os.path.getsize(clip_path)
            print(f"  ✅ {os.path.basename(clip_path)} ({size / 1024:.1f} KB)")
            existing_clips.append(clip_path)
        else:
            print(f"  ❌ {os.path.basename(clip_path)} (not found)")
    
    if not existing_clips:
        print("\n❌ ABORT: No test clips found")
        print("Run test_multi_clip_merge.py first to create test clips")
        sys.exit(1)
    
    print(f"\nUsing {len(existing_clips)} test clips")
    
    # Initialize editor
    print("\n[STAGE 1] Initializing VideoEditor...")
    start_init = time.time()
    
    try:
        editor = VideoEditorRebuilt()
        init_time = time.time() - start_init
        print(f"[STAGE 1] ✅ Initialized in {init_time:.2f}s")
    except Exception as e:
        print(f"[STAGE 1] ❌ ABORT: Initialization failed")
        print(f"Error: {e}")
        sys.exit(1)
    
    # Create video
    print("\n[STAGE 2] Creating video...")
    prompt = "Test video from final pipeline"
    output_filename = "final_pipeline_test_output.mp4"
    
    start_create = time.time()
    
    try:
        output_path = editor.create_video(
            clip_paths=existing_clips,
            prompt=prompt,
            output_filename=output_filename
        )
        
        create_time = time.time() - start_create
        print(f"\n[STAGE 2] ✅ Video created in {create_time:.2f}s")
        
    except Exception as e:
        print(f"\n[STAGE 2] ❌ ABORT: Video creation failed")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Verify output
    print("\n[STAGE 3] Final verification...")
    
    if not os.path.exists(output_path):
        print(f"❌ ABORT: Output file not found: {output_path}")
        sys.exit(1)
    
    output_size = os.path.getsize(output_path)
    print(f"File size: {output_size / 1024:.1f} KB ({output_size / 1024 / 1024:.2f} MB)")
    
    # Check minimum size
    if output_size < 200 * 1024:  # 200KB minimum
        print(f"❌ ABORT: File too small (< 200KB)")
        sys.exit(1)
    
    print("✅ File size valid")
    
    # Verify duration
    print("\nVerifying duration...")
    
    try:
        from moviepy import VideoFileClip
        
        verify_clip = VideoFileClip(output_path)
        final_duration = verify_clip.duration
        verify_clip.close()
        
        print(f"Duration: {final_duration:.2f}s")
        
        if final_duration <= 0:
            print(f"❌ ABORT: Duration is {final_duration}")
            sys.exit(1)
        
        if final_duration < 5.0:
            print(f"⚠️  WARNING: Duration < 5s ({final_duration:.2f}s)")
            print(f"This may be acceptable depending on input clips")
        
        print("✅ Duration valid")
        
    except Exception as e:
        print(f"❌ ABORT: Failed to verify duration")
        print(f"Error: {e}")
        sys.exit(1)
    
    # Timing summary
    total_time = init_time + create_time
    
    print("\n" + "=" * 60)
    print("TIMING BREAKDOWN")
    print("=" * 60)
    print(f"Initialization:  {init_time:.2f}s")
    print(f"Video Creation:  {create_time:.2f}s")
    print(f"  - Download:    (using cached clips)")
    print(f"  - Normalize:   (included in creation)")
    print(f"  - Load:        (included in creation)")
    print(f"  - Merge:       (included in creation)")
    print(f"  - Export:      (included in creation)")
    print(f"Total:           {total_time:.2f}s")
    print("=" * 60)
    
    # Final checks
    print("\n" + "=" * 60)
    print("FINAL VERIFICATION CHECKLIST")
    print("=" * 60)
    
    checks = [
        ("File exists", os.path.exists(output_path)),
        ("File size > 200KB", output_size >= 200 * 1024),
        ("Duration > 0s", final_duration > 0),
        ("Duration verified", True),
    ]
    
    all_passed = True
    for check_name, passed in checks:
        status = "✅" if passed else "❌"
        print(f"{status} {check_name}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if not all_passed:
        print("\n❌ SOME CHECKS FAILED")
        sys.exit(1)
    
    # Success
    print("\n" + "=" * 60)
    print("✅ PIPELINE VERIFIED")
    print("=" * 60)
    print(f"Output: {output_path}")
    print(f"Size: {output_size / 1024 / 1024:.2f} MB")
    print(f"Duration: {final_duration:.2f}s")
    print(f"Total time: {total_time:.2f}s")
    print("=" * 60)
    
    print("\n" + "=" * 60)
    print("PLAYBACK TESTING")
    print("=" * 60)
    print("Test the video in:")
    print(f"\n1. VLC Media Player:")
    print(f"   vlc {output_path}")
    print(f"\n2. Browser:")
    print(f"   file://{os.path.abspath(output_path)}")
    print(f"\n3. Windows Media Player:")
    print(f"   start {output_path}")
    print("=" * 60)
    
    print("\n✅ If video plays in VLC and browser, system is STABLE")
    
    return output_path

if __name__ == "__main__":
    try:
        output_path = final_pipeline_test()
        print(f"\n✅ FINAL TEST SUCCESS: {output_path}")
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n❌ ABORTED BY USER")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ FINAL TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
