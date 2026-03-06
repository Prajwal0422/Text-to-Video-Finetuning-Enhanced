"""
Unified Video Generation CLI
Single command-line interface for all generation methods
"""

import argparse
import sys
import time
from pathlib import Path


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Nexus Vision - Video Generation CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Fast generation
  python video_cli.py fast input.jpg output.mp4
  
  # Ultra-fast generation
  python video_cli.py ultra-fast input.jpg output.mp4
  
  # Smart generation (auto-selects best method)
  python video_cli.py smart input.jpg output.mp4 --priority balanced
  
  # Batch generation
  python video_cli.py batch "images/*.jpg" output_dir/
  
  # Quality generation
  python video_cli.py quality input.jpg output.mp4 --motion ken_burns
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Generation method')
    
    # Fast command
    fast_parser = subparsers.add_parser('fast', help='Fast generation (5-8s)')
    fast_parser.add_argument('image', help='Input image')
    fast_parser.add_argument('output', help='Output video')
    fast_parser.add_argument('--motion', default='auto', help='Motion type')
    fast_parser.add_argument('--duration', type=int, default=3, help='Duration (seconds)')
    
    # Ultra-fast command
    ultra_parser = subparsers.add_parser('ultra-fast', help='Ultra-fast generation (2-3s)')
    ultra_parser.add_argument('image', help='Input image')
    ultra_parser.add_argument('output', help='Output video')
    ultra_parser.add_argument('--duration', type=int, default=3, help='Duration (seconds)')
    ultra_parser.add_argument('--fps', type=int, default=15, help='FPS')
    
    # Smart command
    smart_parser = subparsers.add_parser('smart', help='Smart generation (auto-select)')
    smart_parser.add_argument('image', help='Input image')
    smart_parser.add_argument('output', help='Output video')
    smart_parser.add_argument('--priority', choices=['speed', 'balanced', 'quality'],
                             default='balanced', help='Priority')
    smart_parser.add_argument('--motion', default='auto', help='Motion type')
    smart_parser.add_argument('--duration', type=int, default=3, help='Duration (seconds)')
    
    # Batch command
    batch_parser = subparsers.add_parser('batch', help='Batch generation')
    batch_parser.add_argument('pattern', help='Input pattern (e.g., "images/*.jpg")')
    batch_parser.add_argument('output_dir', help='Output directory')
    batch_parser.add_argument('--workers', type=int, default=4, help='Parallel workers')
    batch_parser.add_argument('--motion', default='auto', help='Motion type')
    batch_parser.add_argument('--duration', type=int, default=3, help='Duration (seconds)')
    
    # Quality command
    quality_parser = subparsers.add_parser('quality', help='Quality generation (15-20s)')
    quality_parser.add_argument('image', help='Input image')
    quality_parser.add_argument('output', help='Output video')
    quality_parser.add_argument('--motion', default='zoom_in', help='Motion type')
    quality_parser.add_argument('--duration', type=int, default=3, help='Duration (seconds)')
    quality_parser.add_argument('--fps', type=int, default=60, help='FPS')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    print("=" * 60)
    print("NEXUS VISION - Video Generation CLI")
    print("=" * 60)
    
    start_time = time.time()
    
    try:
        if args.command == 'fast':
            from fast_video_tool import FastVideoTool
            tool = FastVideoTool()
            result = tool.generate_fast(args.image, args.output, args.motion, args.duration)
            
        elif args.command == 'ultra-fast':
            from ultra_fast_generator import UltraFastGenerator
            generator = UltraFastGenerator()
            generator.generate_ultra_fast(args.image, args.output, args.duration, args.fps)
            result = {'success': True, 'video_path': args.output}
            
        elif args.command == 'smart':
            from smart_video_generator import SmartVideoGenerator
            generator = SmartVideoGenerator()
            result = generator.generate(args.image, args.output, args.priority, args.motion, args.duration)
            
        elif args.command == 'batch':
            from batch_video_generator import BatchVideoGenerator
            import glob
            
            images = glob.glob(args.pattern)
            if not images:
                print(f"❌ No images found: {args.pattern}")
                return
            
            generator = BatchVideoGenerator(max_workers=args.workers)
            result = generator.generate_batch(images, args.output_dir, args.motion, args.duration)
            
        elif args.command == 'quality':
            from enhanced_motion_engine import EnhancedMotionEngine
            from PIL import Image
            
            engine = EnhancedMotionEngine(quality_mode="quality")
            image = Image.open(args.image)
            engine.create_video(
                image, args.output,
                duration=args.duration,
                fps=args.fps,
                motion_type=args.motion,
                apply_effects=True,
                stabilize=True
            )
            result = {'success': True, 'video_path': args.output}
        
        elapsed = time.time() - start_time
        
        if result.get('success'):
            print(f"\n✅ Success!")
            print(f"⏱️  Total time: {elapsed:.2f}s")
            if 'video_path' in result:
                print(f"📹 Output: {result['video_path']}")
        else:
            print(f"\n❌ Failed: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
