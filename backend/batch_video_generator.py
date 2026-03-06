"""
Batch Video Generator
Process multiple images in parallel for maximum throughput
"""

import os
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed
from fast_video_tool import FastVideoTool
import logging

logger = logging.getLogger(__name__)


class BatchVideoGenerator:
    """
    Batch process multiple images into videos
    
    Features:
    - Parallel processing
    - Progress tracking
    - Error handling per item
    - Performance statistics
    """
    
    def __init__(self, max_workers: int = 4):
        """
        Initialize batch generator
        
        Args:
            max_workers: Number of parallel workers (default: 4)
        """
        self.max_workers = max_workers
        self.tool = FastVideoTool()
        logger.info(f"🔄 Batch generator initialized with {max_workers} workers")
    
    def generate_batch(self, image_paths: List[str], 
                      output_dir: str,
                      motion_type: str = "auto",
                      duration: int = 3) -> Dict:
        """
        Generate videos from multiple images in parallel
        
        Args:
            image_paths: List of input image paths
            output_dir: Directory for output videos
            motion_type: Motion effect type
            duration: Video duration in seconds
            
        Returns:
            Dictionary with batch results and statistics
        """
        os.makedirs(output_dir, exist_ok=True)
        
        results = []
        total_start = time.time()
        
        logger.info(f"🚀 Starting batch generation of {len(image_paths)} videos")
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            futures = {}
            for i, image_path in enumerate(image_paths):
                # Generate output path
                basename = os.path.splitext(os.path.basename(image_path))[0]
                output_path = os.path.join(output_dir, f"{basename}_video.mp4")
                
                # Submit task
                future = executor.submit(
                    self.tool.generate_fast,
                    image_path, output_path, motion_type, duration
                )
                futures[future] = (i, image_path, output_path)
            
            # Collect results as they complete
            completed = 0
            for future in as_completed(futures):
                completed += 1
                i, image_path, output_path = futures[future]
                
                try:
                    result = future.result()
                    result['index'] = i
                    result['input_path'] = image_path
                    results.append(result)
                    
                    if result['success']:
                        logger.info(f"✅ [{completed}/{len(image_paths)}] {os.path.basename(image_path)}")
                    else:
                        logger.error(f"❌ [{completed}/{len(image_paths)}] {os.path.basename(image_path)}: {result.get('error')}")
                        
                except Exception as e:
                    logger.error(f"❌ [{completed}/{len(image_paths)}] {os.path.basename(image_path)}: {e}")
                    results.append({
                        'success': False,
                        'index': i,
                        'input_path': image_path,
                        'error': str(e)
                    })
        
        total_time = time.time() - total_start
        
        # Calculate statistics
        successful = sum(1 for r in results if r['success'])
        failed = len(results) - successful
        avg_time = total_time / len(results) if results else 0
        
        logger.info(f"\n📊 Batch complete in {total_time:.2f}s")
        logger.info(f"   Successful: {successful}/{len(results)}")
        logger.info(f"   Failed: {failed}")
        logger.info(f"   Avg time per video: {avg_time:.2f}s")
        
        return {
            'total_time': total_time,
            'total_videos': len(results),
            'successful': successful,
            'failed': failed,
            'avg_time_per_video': avg_time,
            'results': results
        }


import time

def main():
    """CLI for batch generation"""
    import argparse
    import glob
    
    parser = argparse.ArgumentParser(description='Batch Video Generator')
    parser.add_argument('input_pattern', help='Input image pattern (e.g., "images/*.jpg")')
    parser.add_argument('output_dir', help='Output directory')
    parser.add_argument('--workers', type=int, default=4, help='Number of parallel workers')
    parser.add_argument('--motion', default='auto', help='Motion type')
    parser.add_argument('--duration', type=int, default=3, help='Duration in seconds')
    
    args = parser.parse_args()
    
    # Find images
    image_paths = glob.glob(args.input_pattern)
    
    if not image_paths:
        print(f"❌ No images found matching: {args.input_pattern}")
        return
    
    print(f"📁 Found {len(image_paths)} images")
    
    # Generate batch
    generator = BatchVideoGenerator(max_workers=args.workers)
    result = generator.generate_batch(
        image_paths,
        args.output_dir,
        args.motion,
        args.duration
    )
    
    print(f"\n✅ Batch complete!")
    print(f"   Total time: {result['total_time']:.2f}s")
    print(f"   Successful: {result['successful']}/{result['total_videos']}")


if __name__ == "__main__":
    main()
