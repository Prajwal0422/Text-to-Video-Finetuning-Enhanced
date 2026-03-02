"""
PHASE 1: ENVIRONMENT VERIFICATION
Strict runtime verification of all dependencies
"""

import sys
import os
import subprocess

def verify_environment():
    print("=" * 60)
    print("PHASE 1: ENVIRONMENT VERIFICATION")
    print("=" * 60)
    
    # Python version
    print(f"\n[CHECK 1] Python Version")
    print(f"Version: {sys.version}")
    print(f"Executable: {sys.executable}")
    major, minor = sys.version_info[:2]
    if major < 3 or (major == 3 and minor < 8):
        print("❌ ABORT: Python 3.8+ required")
        sys.exit(1)
    print("✅ PASS")
    
    # MoviePy
    print(f"\n[CHECK 2] MoviePy")
    try:
        import moviepy
        print(f"Version: {moviepy.__version__}")
        print(f"Location: {moviepy.__file__}")
        print("✅ PASS")
    except ImportError as e:
        print(f"❌ ABORT: MoviePy not installed")
        print(f"Error: {e}")
        print("Install: pip install moviepy")
        sys.exit(1)
    
    # imageio
    print(f"\n[CHECK 3] imageio")
    try:
        import imageio
        print(f"Version: {imageio.__version__}")
        print(f"Location: {imageio.__file__}")
        print("✅ PASS")
    except ImportError as e:
        print(f"❌ ABORT: imageio not installed")
        print(f"Error: {e}")
        print("Install: pip install imageio")
        sys.exit(1)
    
    # imageio-ffmpeg
    print(f"\n[CHECK 4] imageio-ffmpeg")
    try:
        import imageio_ffmpeg
        ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
        print(f"FFmpeg Path: {ffmpeg_path}")
        print(f"Location: {imageio_ffmpeg.__file__}")
        
        if not os.path.exists(ffmpeg_path):
            print(f"❌ ABORT: FFmpeg executable not found at {ffmpeg_path}")
            sys.exit(1)
        
        print("✅ PASS")
    except ImportError as e:
        print(f"❌ ABORT: imageio-ffmpeg not installed")
        print(f"Error: {e}")
        print("Install: pip install imageio-ffmpeg")
        sys.exit(1)
    except Exception as e:
        print(f"❌ ABORT: Cannot get FFmpeg path")
        print(f"Error: {e}")
        sys.exit(1)
    
    # FFmpeg execution test
    print(f"\n[CHECK 5] FFmpeg Execution")
    try:
        result = subprocess.run(
            [ffmpeg_path, '-version'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            print(f"❌ ABORT: FFmpeg execution failed")
            print(f"Return code: {result.returncode}")
            print(f"stderr: {result.stderr}")
            sys.exit(1)
        
        # Print first line of version
        version_line = result.stdout.split('\n')[0]
        print(f"FFmpeg: {version_line}")
        print("✅ PASS")
        
    except subprocess.TimeoutExpired:
        print(f"❌ ABORT: FFmpeg execution timeout")
        sys.exit(1)
    except FileNotFoundError:
        print(f"❌ ABORT: FFmpeg not found")
        sys.exit(1)
    except Exception as e:
        print(f"❌ ABORT: FFmpeg execution error")
        print(f"Error: {e}")
        sys.exit(1)
    
    # Final summary
    print("\n" + "=" * 60)
    print("✅ ALL ENVIRONMENT CHECKS PASSED")
    print("=" * 60)
    print(f"Python: {major}.{minor}")
    print(f"MoviePy: {moviepy.__version__}")
    print(f"imageio: {imageio.__version__}")
    print(f"FFmpeg: {ffmpeg_path}")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    try:
        verify_environment()
    except KeyboardInterrupt:
        print("\n❌ ABORTED BY USER")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
