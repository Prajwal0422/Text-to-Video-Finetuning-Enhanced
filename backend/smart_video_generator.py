"""
Smart Video Generator
Automatically selects best generation method based on requirements
"""

from typing import Dict, Optional
from .fast_video_tool import FastVideoTool
from .ultra_fast_generator import UltraFastGenerator
from .enhanced_motion_engine import EnhancedMotionEngine
from .quality_analyzer import QualityAnalyzer
from PIL import Image
import logging

logger = logging.getLogger(__name__)


class SmartVideoGenerator:
    """
    Intelligent video generator that automatically selects
    the best generation method based on:
    - Image complexity
    - Quality requirements
    - Speed requirements
    - Available resources (GPU)
    """
    
    def __init__(self):
        self.fast_tool = FastVideoTool()
        self.ultra_fast = UltraFastGenerator()
    
    def generate(self, image_path: str, output_path: str,
                priority: str = "balanced",
                motion_type: str = "auto",
                duration: int = 3) -> Dict:
        """
        Generate video with smart method selection
        
        Args:
            image_path: Input image path
            output_path: Output video path
            priority: "speed", "balanced", or "quality"
            motion_type: Motion effect type
            duration: Video duration in seconds
            
        Returns:
            Generation results with method used
        """
        # Analyze image
        image = Image.open(image_path)
        analysis = QualityAnalyzer.recommend_settings(image)
        
        logger.info(f"🧠 Smart analysis:")
        logger.info(f"   Complexity: {analysis['complexity_score']:.2f}")
        logger.info(f"   Recommended: {analysis['quality_mode']}")
        
        # Select method based on priority
        if priority == "speed":
            # Ultra-fast method (2-3 seconds)
            logger.info("⚡ Using ultra-fast method")
            self.ultra_fast.generate_ultra_fast(
                image_path, output_path, duration
            )
            method = "ultra_fast"
            
        elif priority == "quality":
            # High-quality method (15-20 seconds)
            logger.info("🎨 Using quality method")
            engine = EnhancedMotionEngine(quality_mode="quality")
            engine.create_video(
                image, output_path,
                duration=duration,
                fps=60,
                motion_type=motion_type,
                apply_effects=True,
                stabilize=True
            )
            method = "quality"
            
        else:  # balanced
            # Fast method with good quality (5-8 seconds)
            logger.info("⚖️  Using balanced method")
            result = self.fast_tool.generate_fast(
                image_path, output_path, motion_type, duration
            )
            method = "balanced"
        
        return {
            'success': True,
            'method': method,
            'analysis': analysis,
            'output_path': output_path
        }


def main():
    """CLI for smart generator"""
    import argparse
    import time
    
    parser = argparse.ArgumentParser(description='Smart Video Generator')
    parser.add_argument('image', help='Input image')
    parser.add_argument('output', help='Output video')
    parser.add_argument('--priority', choices=['speed', 'balanced', 'quality'],
                       default='balanced', help='Generation priority')
    parser.add_argument('--motion', default='auto', help='Motion type')
    parser.add_argument('--duration', type=int, default=3, help='Duration')
    
    args = parser.parse_args()
    
    generator = SmartVideoGenerator()
    
    start = time.time()
    result = generator.generate(
        args.image,
        args.output,
        args.priority,
        args.motion,
        args.duration
    )
    elapsed = time.time() - start
    
    print(f"\n✅ Generated using {result['method']} method in {elapsed:.2f}s")
    print(f"📹 Output: {result['output_path']}")


if __name__ == "__main__":
    main()
