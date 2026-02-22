"""
MINIMAL STABLE VIDEO PIPELINE - Single Clip Test
================================================
Purpose: Verify core video processing works without complexity
Author: Senior Video Systems Engineer
Date: 2026-02-22

This script tests the absolute minimum viable pipeline:
1. Download ONE clip
2. Normalize with FFmpeg
3. Load in MoviePy
4. Trim safely
5. Export

NO complexity. NO fancy features. Just stability.
"""

import os
import sys
import requests
import subprocess
from moviepy import VideoFileClip

# ============================================
# CONFIGURATION
# ============================================

PEXELS_API_KEY = os.getenv('PEXELS_API_KEY', '')
TEST_KEYWORD = "ocean"
OUTPUT_DIR = "outputs/test"
DOWNLOAD_PATH = os.path.join(OUTPUT_DIR, "downloaded.mp4")
NORMALIZED_PATH = os.path.join(OUTPUT_DIR, "normalized.mp4")
FINAL_PATH = os.path.join(OUTPUT_DIR, "final_test.mp4")

MIN_FILE_SIZE = 100 * 1024  # 100KB
MIN_DURATION = 1.0
TARGET_DURATION = 3.0
TARGET_FPS = 24

# ============================================
# STEP 1: DOWNLOAD SINGLE CLIP
# ============================================

def download_single_clip():
    """Download ONE small clip from Pexels"""
    print("\n" + "="*60)
    print("STEP 1: DOWNLOADING SINGLE CLIP")
    print("="*60)
    
    if not PEXELS_API_KEY:
        print("❌ ERROR: No PEXELS_API_KEY found")
        print("   Set with: export PEXELS_API_KEY='your_key'")
        return False
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Search for video
    print(f"🔍 Searching Pexels for: {TEST_KEYWORD}")
    
    try:
        headers = {'Authorization': PEXELS_API_KEY}
        params = {
            'query': TEST_KEYWORD,
            'per_page': 1,
            'orientation': 'landscape',
            'size': 'small'
        }
        
        response = requests.get(
            'https://api.pexels.com/videos/search',
            headers=headers,
            params=params,
            timeout=10
        )
        
        if response.status_code != 200:
            print(f"❌ API Error: {response.status_code}")
            return False
        
        data = response.json()
        videos = data.get('videos', [])
        
        if not videos:
            print(f"❌ No videos found for: {TEST_KEYWORD}")
            return False
        
        video = videos[0]
        video_files = video.get('video_files', [])
        
        if not video_files:
            print("❌ No video files in response")
            return False
        
        # Select smallest video file
        video_files.sort(key=lambda x: x.get('width', 9999))
        selected = video_files[0]
        video_url = selected.get('link')
        
        if not video_url:
            print("❌ No video URL found")
            return False
        
        print(f"✅ Found video: {selected.get('width')}x{selected.get('height')}")
        print(f"📥 Downloading from: {video_url[:50]}...")
        
        # Download with streaming
        response = requests.get(video_url, stream=True, timeout=30)
        
        if response.status_code != 200:
            print(f"❌ Download failed: {response.status_code}")
            return False
        
        # Save to file
        downloaded_bytes = 0
        with open(DOWNLOAD_PATH, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024*1024):
                if chunk:
                    f.write(chunk)
                    downloaded_bytes += len(chunk)
        
        print(f"✅ Downloaded: {downloaded_bytes / 1024:.1f} KB")
        
        # Verify file size
        if not os.path.exists(DOWNLOAD_PATH):
            print("❌ File not created")
            return False
        
        file_size = os.path.getsize(DOWNLOAD_PATH)
        
        if file_size < MIN_FILE_SIZE:
            print(f"❌ File too small: {file_size} bytes (min: {MIN_FILE_SIZE})")
            return False
        
        print(f"✅ File size OK: {file_size / 1024:.1f} KB")
        return True
        
    except requests.Timeout:
        print("❌ Request timeout")
        return False
    except Exception as e:
        print(f"❌ Download error: {e}")
        import traceback
        traceback.print_exc()
        return False


# ============================================
# STEP 2: NORMALIZE WITH FFMPEG
# ============================================

def normalize_with_ffmpeg():
    """Normalize video using FFmpeg subprocess"""
    print("\n" + "="*60)
    print("STEP 2: NORMALIZING WITH FFMPEG")
    print("="*60)
    
    if not os.path.exists(DOWNLOAD_PATH):
        print("❌ Downloaded file not found")
        return False
    
    print(f"🔧 Input: {DOWNLOAD_PATH}")
    print(f"🔧 Output: {NORMALIZED_PATH}")
    print("🔧 Command: ffmpeg -y -i input.mp4 -vf scale=640:-2 -r 24 -an output.mp4")
    
    try:
        # Build FFmpeg command
        cmd = [
            'ffmpeg',
            '-y',  # Overwrite output
            '-i', DOWNLOAD_PATH,
            '-vf', 'scale=640:-2',  # Scale to 640 width, auto height (even)
            '-r', '24',  # 24 fps
            '-an',  # No audio
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-crf', '23',
            NORMALIZED_PATH
        ]
        
        print("⚙️  Running FFmpeg...")
        
        # Run FFmpeg
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode != 0:
            print(f"❌ FFmpeg failed with code: {result.returncode}")
            print(f"   stderr: {result.stderr[:500]}")
            return False
        
        print("✅ FFmpeg completed")
        
        # Verify normalized file
        if not os.path.exists(NORMALIZED_PATH):
            print("❌ Normalized file not created")
            return False
        
        file_size = os.path.getsize(NORMALIZED_PATH)
        
        if file_size < MIN_FILE_SIZE:
            print(f"❌ Normalized file too small: {file_size} bytes")
            return False
        
        print(f"✅ Normalized file OK: {file_size / 1024:.1f} KB")
        return True
        
    except subprocess.TimeoutExpired:
        print("❌ FFmpeg timeout (60s)")
        return False
    except FileNotFoundError:
        print("❌ FFmpeg not found - install ffmpeg")
        print("   Windows: pip install imageio-ffmpeg")
        print("   Linux: sudo apt-get install ffmpeg")
        print("   Mac: brew install ffmpeg")
        return False
    except Exception as e:
        print(f"❌ FFmpeg error: {e}")
        import traceback
        traceback.print_exc()
        return False


# ============================================
# STEP 3: LOAD AND VALIDATE IN MOVIEPY
# ============================================

def load_and_validate():
    """Load normalized video in MoviePy and validate"""
    print("\n" + "="*60)
    print("STEP 3: LOADING IN MOVIEPY")
    print("="*60)
    
    if not os.path.exists(NORMALIZED_PATH):
        print("❌ Normalized file not found")
        return None
    
    try:
        print(f"📂 Loading: {NORMALIZED_PATH}")
        
        # Load video
        clip = VideoFileClip(NORMALIZED_PATH)
        
        print(f"✅ Loaded successfully")
        print(f"📊 Duration: {clip.duration:.2f} seconds")
        print(f"📊 Size: {clip.size}")
        print(f"📊 FPS: {clip.fps}")
        
        # Validate duration
        if clip.duration < MIN_DURATION:
            print(f"❌ Duration too short: {clip.duration:.2f}s (min: {MIN_DURATION}s)")
            clip.close()
            return None
        
        print(f"✅ Duration OK: {clip.duration:.2f}s")
        return clip
        
    except Exception as e:
        print(f"❌ MoviePy load error: {e}")
        import traceback
        traceback.print_exc()
        return None


# ============================================
# STEP 4: TRIM SAFELY
# ============================================

def trim_clip(clip):
    """Trim clip to target duration safely"""
    print("\n" + "="*60)
    print("STEP 4: TRIMMING CLIP")
    print("="*60)
    
    try:
        original_duration = clip.duration
        print(f"📏 Original duration: {original_duration:.2f}s")
        
        # Calculate safe end time
        safe_end = min(TARGET_DURATION, clip.duration)
        print(f"✂️  Trimming to: {safe_end:.2f}s")
        
        # Trim if needed
        if safe_end < clip.duration:
            clip = clip.subclipped(0, safe_end)
            print(f"✅ Trimmed to: {clip.duration:.2f}s")
        else:
            print(f"✅ No trim needed (clip is {clip.duration:.2f}s)")
        
        # Verify trimmed duration
        if clip.duration <= 0:
            print("❌ Clip has 0 duration after trim")
            return None
        
        print(f"✅ Final duration: {clip.duration:.2f}s")
        return clip
        
    except Exception as e:
        print(f"❌ Trim error: {e}")
        import traceback
        traceback.print_exc()
        return None


# ============================================
# STEP 5: EXPORT FINAL VIDEO
# ============================================

def export_video(clip):
    """Export final video with stable settings"""
    print("\n" + "="*60)
    print("STEP 5: EXPORTING FINAL VIDEO")
    print("="*60)
    
    try:
        print(f"💾 Output path: {FINAL_PATH}")
        print(f"⚙️  Settings:")
        print(f"   - codec: libx264")
        print(f"   - fps: {TARGET_FPS}")
        print(f"   - preset: medium")
        print(f"   - threads: 4")
        print(f"   - audio: False")
        
        print("\n🎬 Exporting... (this may take 10-30 seconds)")
        
        # Export with stable settings
        clip.write_videofile(
            FINAL_PATH,
            codec='libx264',
            fps=TARGET_FPS,
            preset='medium',
            threads=4,
            audio=False,
            logger=None  # Suppress MoviePy logs
        )
        
        print("\n✅ Export completed")
        
        # Verify output file
        if not os.path.exists(FINAL_PATH):
            print("❌ Output file not created")
            return False
        
        file_size = os.path.getsize(FINAL_PATH)
        
        if file_size < MIN_FILE_SIZE:
            print(f"❌ Output file too small: {file_size} bytes")
            return False
        
        print(f"✅ Output file OK: {file_size / 1024:.1f} KB")
        
        # Verify with MoviePy
        print("\n🔍 Verifying output...")
        test_clip = VideoFileClip(FINAL_PATH)
        print(f"✅ Output duration: {test_clip.duration:.2f}s")
        print(f"✅ Output size: {test_clip.size}")
        test_clip.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Export error: {e}")
        import traceback
        traceback.print_exc()
        return False


# ============================================
# MAIN PIPELINE
# ============================================

def main():
    """Run the complete minimal stable pipeline"""
    print("\n" + "="*60)
    print("MINIMAL STABLE VIDEO PIPELINE - SINGLE CLIP TEST")
    print("="*60)
    print("Goal: Verify core video processing works")
    print("Complexity: MINIMAL")
    print("="*60)
    
    clip = None
    
    try:
        # Step 1: Download
        if not download_single_clip():
            print("\n❌ FAILED at Step 1: Download")
            return False
        
        # Step 2: Normalize
        if not normalize_with_ffmpeg():
            print("\n❌ FAILED at Step 2: FFmpeg Normalization")
            return False
        
        # Step 3: Load
        clip = load_and_validate()
        if clip is None:
            print("\n❌ FAILED at Step 3: MoviePy Load")
            return False
        
        # Step 4: Trim
        clip = trim_clip(clip)
        if clip is None:
            print("\n❌ FAILED at Step 4: Trim")
            return False
        
        # Step 5: Export
        if not export_video(clip):
            print("\n❌ FAILED at Step 5: Export")
            return False
        
        # Success!
        print("\n" + "="*60)
        print("✅ SUCCESS - PIPELINE COMPLETED")
        print("="*60)
        print(f"📹 Final video: {FINAL_PATH}")
        print(f"📊 Test this file in a video player")
        print("="*60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Cleanup
        if clip is not None:
            try:
                clip.close()
                print("\n🧹 Cleaned up MoviePy resources")
            except:
                pass


# ============================================
# ENTRY POINT
# ============================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("STARTING MINIMAL STABLE VIDEO PIPELINE TEST")
    print("="*60)
    
    # Check Python version
    print(f"Python: {sys.version}")
    
    # Check API key
    if not PEXELS_API_KEY:
        print("\n⚠️  WARNING: No PEXELS_API_KEY set")
        print("   Set with: export PEXELS_API_KEY='your_key'")
        print("   Get key at: https://www.pexels.com/api/")
        sys.exit(1)
    
    # Run pipeline
    success = main()
    
    # Exit with appropriate code
    if success:
        print("\n✅ TEST PASSED - Video pipeline is stable")
        sys.exit(0)
    else:
        print("\n❌ TEST FAILED - Check errors above")
        sys.exit(1)
