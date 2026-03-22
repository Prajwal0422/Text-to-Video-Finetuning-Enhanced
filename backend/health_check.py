"""
Health Check Utility
Verifies all system components are working
"""

import os
import sys

def check_ffmpeg():
    """Check if FFmpeg is available"""
    try:
        import imageio_ffmpeg
        ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
        if os.path.exists(ffmpeg_path):
            print("✅ FFmpeg: Available")
            return True
        else:
            print("❌ FFmpeg: Not found")
            return False
    except Exception as e:
        print(f"❌ FFmpeg: Error - {e}")
        return False

def check_moviepy():
    """Check if MoviePy is available"""
    try:
        from moviepy import VideoFileClip
        print("✅ MoviePy: Available")
        return True
    except Exception as e:
        print(f"❌ MoviePy: Error - {e}")
        return False

def check_directories():
    """Check if required directories exist"""
    dirs = ['outputs/videos', 'outputs/cache', 'outputs/normalized']
    all_exist = True
    for d in dirs:
        if os.path.exists(d):
            print(f"✅ Directory: {d}")
        else:
            print(f"❌ Directory: {d} (missing)")
            all_exist = False
    return all_exist

def check_api_key():
    """Check if API key is configured"""
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('PEXELS_API_KEY')
    if api_key and len(api_key) > 10:
        print("✅ API Key: Configured")
        return True
    else:
        print("❌ API Key: Not configured")
        return False

def run_health_check():
    """Run all health checks"""
    print("=" * 60)
    print("SYSTEM HEALTH CHECK")
    print("=" * 60)
    
    checks = [
        check_ffmpeg(),
        check_moviepy(),
        check_directories(),
        check_api_key()
    ]
    
    print("\n" + "=" * 60)
    if all(checks):
        print("✅ ALL CHECKS PASSED")
        return True
    else:
        print("❌ SOME CHECKS FAILED")
        return False

if __name__ == "__main__":
    success = run_health_check()
    sys.exit(0 if success else 1)
