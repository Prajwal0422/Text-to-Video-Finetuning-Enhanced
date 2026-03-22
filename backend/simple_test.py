"""
Simple Video Generation Test
Tests the complete pipeline with a basic prompt
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.video_generator import VideoGenerator

def test_simple_generation():
    """Test with a simple prompt"""
    print("=" * 60)
    print("SIMPLE VIDEO GENERATION TEST")
    print("=" * 60)
    
    # Initialize generator
    print("\n1. Initializing generator...")
    generator = VideoGenerator()
    print("✅ Generator initialized")
    
    # Test prompt
    prompt = "ocean waves on beach"
    print(f"\n2. Testing prompt: '{prompt}'")
    
    # Progress callback
    def progress(percent, message):
        print(f"[{percent}%] {message}")
    
    # Generate
    print("\n3. Starting generation...")
    result = generator.generate(prompt, progress_callback=progress)
    
    # Results
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    
    if result['success']:
        print(f"✅ SUCCESS")
        print(f"   Video: {result['video_path']}")
        print(f"   Duration: {result['duration']:.1f}s")
        
        # Check file exists
        if os.path.exists(result['video_path']):
            size = os.path.getsize(result['video_path'])
            print(f"   Size: {size / 1024 / 1024:.2f} MB")
        else:
            print(f"   ⚠️  File not found!")
    else:
        print(f"❌ FAILED")
        print(f"   Error: {result['message']}")
    
    print("=" * 60)

if __name__ == "__main__":
    test_simple_generation()
