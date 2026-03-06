"""
Project Startup Script
Verifies environment and starts the video generation system
"""

import sys
import os

print("=" * 70)
print(" " * 15 + "NEXUS VISION - VIDEO GENERATION SYSTEM")
print("=" * 70)

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

print("\n🔍 Verifying system...")

# Run system test
try:
    from backend import test_system
    test_system.main()
    print("\n✅ System verification passed!")
except Exception as e:
    print(f"\n❌ System verification failed: {e}")
    sys.exit(1)

print("\n" + "=" * 70)
print("SYSTEM READY!")
print("=" * 70)

print("\n📚 Available Tools:")
print("   1. Fast Video Tool      - python backend/fast_video_tool.py")
print("   2. Ultra-Fast Generator - python backend/ultra_fast_generator.py")
print("   3. Smart Generator      - python backend/smart_video_generator.py")
print("   4. Batch Generator      - python backend/batch_video_generator.py")
print("   5. Unified CLI          - python backend/video_cli.py")

print("\n📖 Quick Examples:")
print("   # Fast generation")
print("   python backend/video_cli.py fast input.jpg output.mp4")
print()
print("   # Ultra-fast generation")
print("   python backend/video_cli.py ultra-fast input.jpg output.mp4")
print()
print("   # Smart generation")
print("   python backend/video_cli.py smart input.jpg output.mp4 --priority balanced")
print()
print("   # Batch processing")
print("   python backend/video_cli.py batch \"images/*.jpg\" output_dir/")

print("\n" + "=" * 70)
print("Ready to generate videos! 🚀")
print("=" * 70 + "\n")
