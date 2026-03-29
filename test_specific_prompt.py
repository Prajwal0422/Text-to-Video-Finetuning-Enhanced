"""
Test video generation with a specific prompt
"""

import time
from backend.video_generator import VideoGenerator

def test_specific_prompt():
    print("=" * 60)
    print("Testing Specific Prompt Generation")
    print("=" * 60)
    
    gen = VideoGenerator()
    
    # Test with the user's example prompt
    prompt = "two countries doing a war and soldiers struggling to live"
    
    print(f"\nPrompt: {prompt}")
    print("\nGenerating video...")
    
    start_time = time.time()
    
    try:
        result = gen.generate(prompt)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print("\n" + "=" * 60)
        if result.get('success'):
            print("✅ GENERATION SUCCESSFUL")
            print("=" * 60)
            print(f"Video Path: {result['video_path']}")
            print(f"Generation Time: {duration:.2f}s")
            print(f"Message: {result.get('message', 'Video generated successfully')}")
        else:
            print("❌ GENERATION FAILED")
            print("=" * 60)
            print(f"Error: {result.get('message', 'Unknown error')}")
        
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_specific_prompt()
