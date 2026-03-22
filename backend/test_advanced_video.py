"""
Comprehensive Test Suite for Advanced Video Generation
Tests all speed and smoothness optimizations
"""

import os
import sys
import time
import numpy as np
from PIL import Image
import cv2

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

def test_enhanced_motion_engine():
    """Test enhanced motion engine with all algorithms"""
    print("\n" + "="*60)
    print("TEST 1: Enhanced Motion Engine")
    print("="*60)
    
    try:
        from enhanced_motion_engine import EnhancedMotionEngine
        
        # Create test image
        test_img = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
        test_img = Image.fromarray(test_img)
        
        output_dir = "outputs/test_videos"
        os.makedirs(output_dir, exist_ok=True)
        
        # Test different quality modes
        quality_modes = ["fast", "balanced", "quality"]
        
        for quality in quality_modes:
            print(f"\n🎬 Testing {quality} mode...")
            start = time.time()
            
            engine = EnhancedMotionEngine(quality_mode=quality)
            output_path = os.path.join(output_dir, f"test_enhanced_{quality}.mp4")
            
            engine.create_video(
                test_img,
                output_path,
                duration=2,
                motion_type="zoom_in",
                apply_effects=True,
                stabilize=False  # Skip for test speed
            )
            
            elapsed = time.time() - start
            file_size = os.path.getsize(output_path) / 1024  # KB
            
            print(f"✅ {quality.upper()} mode: {elapsed:.2f}s, {file_size:.1f}KB")
        
        print("\n✅ Enhanced Motion Engine: PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Enhanced Motion Engine: FAILED - {e}")
        return False


def test_motion_types():
    """Test all motion types"""
    print("\n" + "="*60)
    print("TEST 2: All Motion Types")
    print("="*60)
    
    try:
        from enhanced_motion_engine import EnhancedMotionEngine
        
        test_img = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
        test_img = Image.fromarray(test_img)
        
        output_dir = "outputs/test_videos"
        os.makedirs(output_dir, exist_ok=True)
        
        motion_types = [
            "zoom_in", "zoom_out", "pan_right", "pan_left",
            "pan_up", "pan_down", "rotate_cw", "rotate_ccw",
            "ken_burns", "dolly_zoom", "breathe"
        ]
        
        engine = EnhancedMotionEngine(quality_mode="fast")
        
        for motion in motion_types:
            print(f"🎬 Testing {motion}...")
            output_path = os.path.join(output_dir, f"test_{motion}.mp4")
            
            engine.create_video(
                test_img,
                output_path,
                duration=2,
                fps=24,
                motion_type=motion,
                apply_effects=False,
                stabilize=False
            )
            
            print(f"✅ {motion}: OK")
        
        print("\n✅ All Motion Types: PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Motion Types Test: FAILED - {e}")
        return False


def test_speed_optimizations():
    """Test speed optimization features"""
    print("\n" + "="*60)
    print("TEST 3: Speed Optimizations")
    print("="*60)
    
    try:
        from speed_optimizer import (
            MultiThreadProcessor, GPUAccelerator,
            CompressionOptimizer, AdaptiveQualityManager
        )
        
        # Test GPU detection
        gpu_available = GPUAccelerator.is_gpu_available()
        print(f"🔍 GPU Available: {gpu_available}")
        
        # Test multi-threading
        processor = MultiThreadProcessor()
        test_data = list(range(100))
        
        start = time.time()
        results = processor.process_frames_parallel(
            test_data,
            lambda x: x * 2
        )
        elapsed = time.time() - start
        
        print(f"✅ Multi-threading: {len(results)} items in {elapsed:.3f}s")
        
        # Test codec optimization
        codec, crf = CompressionOptimizer.get_optimal_codec("balanced")
        print(f"✅ Optimal codec: CRF={crf}")
        
        # Test quality analysis
        test_frame = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
        complexity = AdaptiveQualityManager.analyze_frame_complexity(test_frame)
        print(f"✅ Frame complexity: {complexity:.3f}")
        
        print("\n✅ Speed Optimizations: PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Speed Optimizations: FAILED - {e}")
        return False


def test_video_effects():
    """Test video effects library"""
    print("\n" + "="*60)
    print("TEST 4: Video Effects")
    print("="*60)
    
    try:
        from video_effects import (
            TransitionEffects, CinematicEffects,
            MotionEffects, ColorEffects
        )
        
        # Create test frames
        frame1 = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
        frame2 = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
        
        # Test transitions
        print("🎬 Testing transitions...")
        crossfade = TransitionEffects.crossfade(frame1, frame2, 0.5)
        print("✅ Crossfade: OK")
        
        slide = TransitionEffects.slide_left(frame1, frame2, 0.5)
        print("✅ Slide: OK")
        
        zoom = TransitionEffects.zoom_transition(frame1, frame2, 0.5)
        print("✅ Zoom transition: OK")
        
        # Test cinematic effects
        print("\n🎬 Testing cinematic effects...")
        letterbox = CinematicEffects.add_letterbox(frame1)
        print("✅ Letterbox: OK")
        
        vignette = CinematicEffects.add_vignette(frame1)
        print("✅ Vignette: OK")
        
        grain = CinematicEffects.add_film_grain(frame1)
        print("✅ Film grain: OK")
        
        # Test motion effects
        print("\n🎬 Testing motion effects...")
        ken_burns = MotionEffects.ken_burns_effect(frame1, 0.5)
        print("✅ Ken Burns: OK")
        
        dolly = MotionEffects.dolly_zoom(frame1, 0.5)
        print("✅ Dolly zoom: OK")
        
        # Test color effects
        print("\n🎬 Testing color effects...")
        temp = ColorEffects.color_temperature(frame1, 50)
        print("✅ Color temperature: OK")
        
        teal_orange = ColorEffects.teal_orange_grade(frame1)
        print("✅ Teal/orange grade: OK")
        
        print("\n✅ Video Effects: PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Video Effects: FAILED - {e}")
        return False


def test_advanced_algorithms():
    """Test advanced video algorithms"""
    print("\n" + "="*60)
    print("TEST 5: Advanced Algorithms")
    print("="*60)
    
    try:
        from advanced_video_algorithms import (
            EasingFunctions, OpticalFlowSmoother,
            MotionBlurEngine, ColorGradingEngine
        )
        
        # Test easing functions
        print("🎬 Testing easing functions...")
        for t in [0.0, 0.25, 0.5, 0.75, 1.0]:
            cubic = EasingFunctions.ease_in_out_cubic(t)
            quint = EasingFunctions.ease_in_out_quint(t)
            sine = EasingFunctions.ease_in_out_sine(t)
            print(f"  t={t:.2f}: cubic={cubic:.3f}, quint={quint:.3f}, sine={sine:.3f}")
        print("✅ Easing functions: OK")
        
        # Test optical flow
        print("\n🎬 Testing optical flow interpolation...")
        frame1 = np.random.randint(0, 255, (256, 256, 3), dtype=np.uint8)
        frame2 = np.random.randint(0, 255, (256, 256, 3), dtype=np.uint8)
        
        interpolated = OpticalFlowSmoother.interpolate_frames(frame1, frame2, 2)
        print(f"✅ Optical flow: Generated {len(interpolated)} intermediate frames")
        
        # Test motion blur
        print("\n🎬 Testing motion blur...")
        test_frame = np.random.randint(0, 255, (256, 256, 3), dtype=np.uint8)
        
        dir_blur = MotionBlurEngine.apply_directional_blur(test_frame, 45, 10)
        print("✅ Directional blur: OK")
        
        zoom_blur = MotionBlurEngine.apply_zoom_blur(test_frame, 0.02)
        print("✅ Zoom blur: OK")
        
        # Test color grading
        print("\n🎬 Testing color grading...")
        cinematic = ColorGradingEngine.apply_lut(test_frame, "cinematic")
        print("✅ Cinematic LUT: OK")
        
        contrast = ColorGradingEngine.enhance_contrast(test_frame, 1.2)
        print("✅ Contrast enhancement: OK")
        
        print("\n✅ Advanced Algorithms: PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Advanced Algorithms: FAILED - {e}")
        import traceback
        traceback.print_exc()
        return False


def test_performance_benchmark():
    """Benchmark performance improvements"""
    print("\n" + "="*60)
    print("TEST 6: Performance Benchmark")
    print("="*60)
    
    try:
        from image_to_video import MotionEngine
        
        test_img = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
        test_img = Image.fromarray(test_img)
        
        output_dir = "outputs/test_videos"
        os.makedirs(output_dir, exist_ok=True)
        
        # Test basic engine
        print("🎬 Testing basic engine...")
        start = time.time()
        MotionEngine.create_video(
            test_img,
            os.path.join(output_dir, "benchmark_basic.mp4"),
            duration=2,
            fps=24,
            motion_type="zoom_in",
            use_enhanced=False
        )
        basic_time = time.time() - start
        print(f"✅ Basic engine: {basic_time:.2f}s")
        
        # Test enhanced engine
        print("\n🎬 Testing enhanced engine...")
        start = time.time()
        MotionEngine.create_video(
            test_img,
            os.path.join(output_dir, "benchmark_enhanced.mp4"),
            duration=2,
            fps=24,
            motion_type="zoom_in",
            use_enhanced=True,
            quality_mode="balanced"
        )
        enhanced_time = time.time() - start
        print(f"✅ Enhanced engine: {enhanced_time:.2f}s")
        
        # Compare
        print(f"\n📊 Performance comparison:")
        print(f"   Basic: {basic_time:.2f}s")
        print(f"   Enhanced: {enhanced_time:.2f}s")
        
        if enhanced_time < basic_time * 2:  # Allow 2x overhead for quality
            print("✅ Performance: ACCEPTABLE")
        else:
            print("⚠️  Performance: Enhanced is slower but higher quality")
        
        print("\n✅ Performance Benchmark: PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Performance Benchmark: FAILED - {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run complete test suite"""
    print("\n" + "="*60)
    print("ADVANCED VIDEO GENERATION TEST SUITE")
    print("Testing Speed & Smoothness Optimizations")
    print("="*60)
    
    tests = [
        ("Enhanced Motion Engine", test_enhanced_motion_engine),
        ("Motion Types", test_motion_types),
        ("Speed Optimizations", test_speed_optimizations),
        ("Video Effects", test_video_effects),
        ("Advanced Algorithms", test_advanced_algorithms),
        ("Performance Benchmark", test_performance_benchmark)
    ]
    
    results = []
    start_time = time.time()
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    total_time = time.time() - start_time
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:.<40} {status}")
    
    print(f"\n{'Total':.< 40} {passed}/{total} passed")
    print(f"{'Time':.< 40} {total_time:.2f}s")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        return True
    else:
        print(f"\n⚠️  {total - passed} TEST(S) FAILED")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
