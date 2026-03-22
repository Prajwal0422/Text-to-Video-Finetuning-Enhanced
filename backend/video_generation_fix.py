"""
Video Generation Fix - Diagnostic and Repair Tool
Identifies and fixes common video generation issues
"""

import os
import sys
from typing import Dict, List

def check_dependencies() -> Dict[str, bool]:
    """Check if all required dependencies are installed"""
    results = {}
    
    # Check moviepy
    try:
        import moviepy
        results['moviepy'] = True
    except ImportError:
        results['moviepy'] = False
    
    # Check requests
    try:
        import requests
        results['requests'] = True
    except ImportError:
        results['requests'] = False
    
    # Check imageio_ffmpeg
    try:
        import imageio_ffmpeg
        ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
        results['ffmpeg'] = os.path.exists(ffmpeg_path)
    except:
        results['ffmpeg'] = False
    
    return results

def check_directories() -> Dict[str, bool]:
    """Check if required directories exist"""
    dirs = {
        'outputs': 'outputs',
        'outputs/videos': 'outputs/videos',
        'outputs/clips': 'outputs/clips',
        'outputs/normalized': 'outputs/normalized'
    }
    
    results = {}
    for name, path in dirs.items():
        exists = os.path.exists(path)
        results[name] = exists
        
        if not exists:
            try:
                os.makedirs(path, exist_ok=True)
                results[name] = True
                print(f"✅ Created directory: {path}")
            except Exception as e:
                print(f"❌ Failed to create {path}: {e}")
    
    return results

def check_api_key() -> bool:
    """Check if Pexels API key is configured"""
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('PEXELS_API_KEY')
    
    if not api_key:
        print("❌ PEXELS_API_KEY not found in environment")
        return False
    
    if len(api_key) < 20:
        print("⚠️  PEXELS_API_KEY seems invalid (too short)")
        return False
    
    print(f"✅ API Key configured: {api_key[:10]}...")
    return True

def test_clip_download() -> bool:
    """Test downloading a single clip"""
    try:
        from clip_fetcher import ClipFetcher
        
        fetcher = ClipFetcher()
        print("\n🔍 Testing clip download...")
        
        # Try to fetch a simple clip
        scenes = [{'query': 'ocean waves', 'keywords': ['ocean', 'waves']}]
        clips = fetcher.fetch_clips_for_scenes(scenes)
        
        if clips and len(clips) > 0:
            print(f"✅ Successfully downloaded {len(clips)} clip(s)")
            return True
        else:
            print("❌ No clips downloaded")
            return False
    
    except Exception as e:
        print(f"❌ Clip download failed: {e}")
        return False

def test_video_editor() -> bool:
    """Test video editor initialization"""
    try:
        from video_editor import VideoEditor
        
        editor = VideoEditor()
        print("✅ Video editor initialized successfully")
        return True
    
    except Exception as e:
        print(f"❌ Video editor failed: {e}")
        return False

def run_diagnostics():
    """Run full diagnostic suite"""
    print("=" * 60)
    print("VIDEO GENERATION DIAGNOSTIC TOOL")
    print("=" * 60)
    
    # Check dependencies
    print("\n1. Checking dependencies...")
    deps = check_dependencies()
    for name, status in deps.items():
        icon = "✅" if status else "❌"
        print(f"   {icon} {name}: {'OK' if status else 'MISSING'}")
    
    # Check directories
    print("\n2. Checking directories...")
    dirs = check_directories()
    for name, status in dirs.items():
        icon = "✅" if status else "❌"
        print(f"   {icon} {name}: {'OK' if status else 'MISSING'}")
    
    # Check API key
    print("\n3. Checking API configuration...")
    api_ok = check_api_key()
    
    # Test video editor
    print("\n4. Testing video editor...")
    editor_ok = test_video_editor()
    
    # Test clip download
    print("\n5. Testing clip download...")
    download_ok = test_clip_download()
    
    # Summary
    print("\n" + "=" * 60)
    print("DIAGNOSTIC SUMMARY")
    print("=" * 60)
    
    all_ok = all(deps.values()) and all(dirs.values()) and api_ok and editor_ok
    
    if all_ok:
        print("✅ All checks passed!")
        print("\nVideo generation should work correctly.")
    else:
        print("❌ Some checks failed!")
        print("\nPlease fix the issues above before generating videos.")
    
    print("=" * 60)

if __name__ == "__main__":
    run_diagnostics()
