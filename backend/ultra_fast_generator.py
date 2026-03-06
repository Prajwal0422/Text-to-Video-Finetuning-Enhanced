"""
Ultra Fast Video Generator
Maximum speed optimization with minimal quality trade-off
"""

import cv2
import numpy as np
import imageio
from PIL import Image
import os
from typing import Optional
from gpu_utils import get_gpu_manager


class UltraFastGenerator:
    """
    Ultra-fast video generation (2-3 seconds per video)
    
    Optimizations:
    - Minimal frame count
    - GPU-accelerated resize
    - No interpolation
    - Fast codec
    - Reduced resolution option
    """
    
    def __init__(self):
        self.gpu = get_gpu_manager()
    
    def generate_ultra_fast(self, image_path: str, output_path: str,
                           duration: int = 3,
                           fps: int = 15,
                           max_resolution: int = 720) -> str:
        """
        Generate video with ultra-fast settings
        
        Args:
            image_path: Input image path
            output_path: Output video path
            duration: Duration in seconds (default: 3)
            fps: Frames per second (default: 15 for speed)
            max_resolution: Max height in pixels (default: 720)
            
        Returns:
            Path to generated video
        """
        # Load image
        img = Image.open(image_path)
        img_np = np.array(img)
        h, w = img_np.shape[:2]
        
        # Resize if too large
        if h > max_resolution:
            scale = max_resolution / h
            new_w, new_h = int(w * scale), int(h * scale)
            
            if self.gpu.cuda_available:
                img_np = self.gpu.resize_gpu(img_np, (new_w, new_h))
            else:
                img_np = cv2.resize(img_np, (new_w, new_h), 
                                   interpolation=cv2.INTER_LINEAR)
            
            h, w = new_h, new_w
        
        # Generate minimal frames
        num_frames = duration * fps
        frames = []
        
        for i in range(num_frames):
            t = i / num_frames
            
            # Simple zoom effect
            scale = 1.0 + (t * 0.1)
            new_w, new_h = int(w * scale), int(h * scale)
            
            # Fast resize
            if self.gpu.cuda_available:
                frame = self.gpu.resize_gpu(img_np, (new_w, new_h))
            else:
                frame = cv2.resize(img_np, (new_w, new_h), 
                                  interpolation=cv2.INTER_LINEAR)
            
            # Center crop
            x = (new_w - w) // 2
            y = (new_h - h) // 2
            frame = frame[y:y+h, x:x+w]
            
            frames.append(frame)
        
        # Save with fast settings
        imageio.mimsave(
            output_path,
            frames,
            fps=fps,
            quality=7,  # Lower quality for speed
            codec='libx264',
            pixelformat='yuv420p'
        )
        
        return output_path


def main():
    """CLI for ultra-fast generation"""
    import argparse
    import time
    
    parser = argparse.ArgumentParser(description='Ultra Fast Video Generator')
    parser.add_argument('image', help='Input image')
    parser.add_argument('output', help='Output video')
    parser.add_argument('--duration', type=int, default=3)
    parser.add_argument('--fps', type=int, default=15)
    parser.add_argument('--resolution', type=int, default=720)
    
    args = parser.parse_args()
    
    generator = UltraFastGenerator()
    
    start = time.time()
    output = generator.generate_ultra_fast(
        args.image,
        args.output,
        args.duration,
        args.fps,
        args.resolution
    )
    elapsed = time.time() - start
    
    print(f"✅ Generated in {elapsed:.2f}s: {output}")


if __name__ == "__main__":
    main()
