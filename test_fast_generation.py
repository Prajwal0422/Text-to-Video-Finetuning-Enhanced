"""
Quick test of fast video generation
"""

import time
from backend.fast_video_generator import FastVideoGenerator

def test_fast_generation():
    print("=" * 60)
    print("Testing Fast Video Generation")
    print("=" * 60)
    
    gen = FastVideoGenerator()
    
    # Test prompt
    prompt = "ocean waves at sunset"
    
    print(f"\nPrompt: {prompt}")
    print("\nGenerating in FAST mode...")
    
    start_time = time.time()
    
    try:
        result = gen.generate_fast(prompt)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print("\n" + "=" * 60)
        print("✅ GENERATION SUCCESSFUL")
        print("=" * 60)
        print(f"Video Path: {result['video_path']}")
        print(f"Generation Time: {duration:.2f}s")
        print(f"Target: ~18s")
        
        if duration < 20:
            print("✅ Speed target achieved!")
        else:
            print("⚠️  Slower than expected")
        
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    test_fast_generation()
