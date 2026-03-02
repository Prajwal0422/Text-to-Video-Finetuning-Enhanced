"""
PHASE 2: RAW CLIP VALIDATION
Download and normalize a single clip with strict verification
"""

import os
import sys
import requests
import subprocess
import imageio_ffmpeg

def test_download_and_normalize():
    print("=" * 60)
    print("PHASE 2: RAW CLIP VALIDATION")
    print("=" * 60)
    
    # Setup
    output_dir = "outputs/test_clips"
    os.makedirs(output_dir, exist_ok=True)
    
    raw_path = os.path.join(output_dir, "raw_test_clip.mp4")
    normalized_path = os.path.join(output_dir, "normalized_test_clip.mp4")
    
    # Clean previous test files
    for path in [raw_path, normalized_path]:
        if os.path.exists(path):
            os.remove(path)
            print(f"Cleaned: {path}")
    
    # Step 1: Download clip
    print("\n[STEP 1] Downloading test clip from Pexels")
    
    # Use a known working video URL (small file)
    # This is a direct link to a small Pexels video
    test_url = "https://player.vimeo.com/external/373971162.sd.mp4?s=7c6f0c6f3c3e3c3e3c3e3c3e3c3e3c3e3c3e3c3e&profile_id=164&oauth2_token_id=57447761"
    
    # Fallback: Use Pexels API if available
    api_key = os.getenv('PEXELS_API_KEY', '')
    if api_key:
        print("Using Pexels API to find clip...")
        try:
            headers = {'Authorization': api_key}
            response = requests.get(
                'https://api.pexels.com/videos/search',
                headers=headers,
                params={'query': 'nature', 'per_page': 1, 'orientation': 'landscape'},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                videos = data.get('videos', [])
                if videos:
                    video_files = videos[0].get('video_files', [])
                    # Find smallest file
                    small_files = [vf for vf in video_files if vf.get('width', 9999) <= 640]
                    if small_files:
                        test_url = small_files[0]['link']
                        print(f"Found Pexels video: {test_url[:60]}...")
        except Exception as e:
            print(f"Pexels API failed, using fallback URL: {e}")
    
    print(f"Downloading from: {test_url[:80]}...")
    
    try:
        response = requests.get(test_url, stream=True, timeout=30)
        
        if response.status_code != 200:
            print(f"❌ ABORT: Download failed with status {response.status_code}")
            sys.exit(1)
        
        # Download with streaming
        downloaded = 0
        with open(raw_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
        
        print(f"Downloaded: {downloaded} bytes")
        
    except requests.Timeout:
        print(f"❌ ABORT: Download timeout")
        sys.exit(1)
    except Exception as e:
        print(f"❌ ABORT: Download error: {e}")
        sys.exit(1)
    
    # Step 2: Verify file exists
    print("\n[STEP 2] Verifying downloaded file")
    
    if not os.path.exists(raw_path):
        print(f"❌ ABORT: File not created: {raw_path}")
        sys.exit(1)
    
    file_size = os.path.getsize(raw_path)
    print(f"File size: {file_size} bytes ({file_size / 1024:.1f} KB)")
    
    if file_size < 100 * 1024:  # 100KB minimum
        print(f"❌ ABORT: File too small (< 100KB)")
        print(f"File may be corrupted or incomplete")
        sys.exit(1)
    
    print("✅ PASS: File size valid")
    
    # Step 3: FFmpeg normalization
    print("\n[STEP 3] Running FFmpeg normalization")
    
    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
    
    cmd = [
        ffmpeg_path,
        '-y',  # Overwrite
        '-i', raw_path,
        '-vf', 'scale=640:-2',  # Scale to 640 width, auto height (even)
        '-r', '24',  # 24 fps
        '-an',  # No audio
        '-c:v', 'libx264',  # H.264 codec
        '-preset', 'fast',
        '-crf', '23',
        normalized_path
    ]
    
    print(f"Command: {' '.join(cmd[:8])}...")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode != 0:
            print(f"❌ ABORT: FFmpeg normalization failed")
            print(f"Return code: {result.returncode}")
            print(f"stderr: {result.stderr[-500:]}")  # Last 500 chars
            sys.exit(1)
        
        print("FFmpeg completed successfully")
        
    except subprocess.TimeoutExpired:
        print(f"❌ ABORT: FFmpeg timeout (60s)")
        sys.exit(1)
    except Exception as e:
        print(f"❌ ABORT: FFmpeg error: {e}")
        sys.exit(1)
    
    # Step 4: Verify normalized file
    print("\n[STEP 4] Verifying normalized file")
    
    if not os.path.exists(normalized_path):
        print(f"❌ ABORT: Normalized file not created")
        sys.exit(1)
    
    normalized_size = os.path.getsize(normalized_path)
    print(f"Normalized size: {normalized_size} bytes ({normalized_size / 1024:.1f} KB)")
    
    if normalized_size < 10 * 1024:  # 10KB minimum
        print(f"❌ ABORT: Normalized file too small (< 10KB)")
        sys.exit(1)
    
    print("✅ PASS: Normalized file valid")
    
    # Final summary
    print("\n" + "=" * 60)
    print("✅ PHASE 2 COMPLETE: RAW CLIP VALIDATED")
    print("=" * 60)
    print(f"Raw file: {raw_path}")
    print(f"Raw size: {file_size / 1024:.1f} KB")
    print(f"Normalized file: {normalized_path}")
    print(f"Normalized size: {normalized_size / 1024:.1f} KB")
    print("=" * 60)
    
    return normalized_path

if __name__ == "__main__":
    try:
        normalized_path = test_download_and_normalize()
        print(f"\n✅ SUCCESS: {normalized_path}")
    except KeyboardInterrupt:
        print("\n❌ ABORTED BY USER")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
