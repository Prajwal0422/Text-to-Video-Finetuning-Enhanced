"""
Test Video Generation
Quick test to verify video generation works
"""

import sys
sys.path.insert(0, '.')

from video_generator import VideoGenerator

def test_generation():
    print("=" * 60)
    print("Testing Video Generation")
    print("=" * 60)
    
    generator = VideoGenerator()
    
    test_prompts = [
        "sunset over ocean",
        "city at night",
        "mountain landscape"
    ]
    
    for prompt in test_prompts:
        print(f"\nTesting: '{prompt}'")
        result = generator.generate(prompt)
        
        if result['success']:
            print(f"✅ SUCCESS - {result['video_path']}")
        else:
            print(f"❌ FAILED - {result['message']}")

if __name__ == "__main__":
    test_generation()
