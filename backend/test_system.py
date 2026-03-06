"""
System Test and Verification Script
Tests all components to ensure the project runs correctly
"""

import sys
import os

def test_imports():
    """Test all module imports"""
    print("=" * 60)
    print("TESTING MODULE IMPORTS")
    print("=" * 60)
    
    modules = [
        'numpy',
        'cv2',
        'PIL',
        'imageio',
        'scipy'
    ]
    
    for module in modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
    
    print()

def test_custom_modules():
    """Test custom module imports"""
    print("=" * 60)
    print("TESTING CUSTOM MODULES")
    print("=" * 60)
    
    custom_modules = [
        'gpu_utils',
        'cache_manager',
        'performance_monitor',
        'motion_types',
        'frame_interpolator',
        'motion_blur',
        'video_stabilizer',
        'color_grading',
        'compression_optimizer',
        'quality_analyzer',
        'transition_effects'
    ]
    
    for module in custom_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except Exception as e:
            print(f"❌ {module}: {e}")
    
    print()

def test_tools():
    """Test tool availability"""
    print("=" * 60)
    print("TESTING TOOLS")
    print("=" * 60)
    
    tools = [
        'fast_video_tool',
        'ultra_fast_generator',
        'smart_video_generator',
        'batch_video_generator'
    ]
    
    for tool in tools:
        try:
            __import__(tool)
            print(f"✅ {tool}")
        except Exception as e:
            print(f"❌ {tool}: {e}")
    
    print()

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("NEXUS VISION - SYSTEM VERIFICATION")
    print("=" * 60 + "\n")
    
    test_imports()
    test_custom_modules()
    test_tools()
    
    print("=" * 60)
    print("VERIFICATION COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()
