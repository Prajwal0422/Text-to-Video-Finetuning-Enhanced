"""
Video Compression Utility
Compress videos for faster delivery and storage
"""

import os
import subprocess
from typing import Optional, Dict
import imageio_ffmpeg

class VideoCompressor:
    def __init__(self):
        self.ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
        
        # Compression presets
        self.presets = {
            'high': {
                'crf': 18,
                'preset': 'slow',
                'description': 'High quality, larger file'
            },
            'medium': {
                'crf': 23,
                'preset': 'medium',
                'description': 'Balanced quality and size'
            },
            'low': {
                'crf': 28,
                'preset': 'fast',
                'description': 'Lower quality, smaller file'
            },
            'web': {
                'crf': 26,
                'preset': 'fast',
                'max_width': 854,
                'description': 'Optimized for web delivery'
            },
            'mobile': {
                'crf': 28,
                'preset': 'fast',
                'max_width': 640,
                'description': 'Optimized for mobile devices'
            }
        }
    
    def compress(self, input_path: str, output_path: Optional[str] = None,
                preset: str = 'medium') -> Dict:
        """Compress video with specified preset"""
        if not os.path.exists(input_path):
            return {'error': 'Input file not found'}
        
        if preset not in self.presets:
            return {'error': f'Invalid preset. Choose from: {list(self.presets.keys())}'}
        
        # Generate output path if not provided
        if not output_path:
            base, ext = os.path.splitext(input_path)
            output_path = f"{base}_compressed{ext}"
        
        # Get preset settings
        settings = self.presets[preset]
        
        # Build FFmpeg command
        cmd = [
            self.ffmpeg_path,
            '-y',  # Overwrite
            '-i', input_path,
            '-c:v', 'libx264',
            '-crf', str(settings['crf']),
            '-preset', settings['preset']
        ]
        
        # Add resolution limit if specified
        if 'max_width' in settings:
            cmd.extend(['-vf', f"scale='min({settings['max_width']},iw)':-2"])
        
        # No audio
        cmd.extend(['-an', output_path])
        
        try:
            # Get input file size
            input_size = os.path.getsize(input_path)
            
            # Run compression
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode != 0:
                return {'error': f'Compression failed: {result.stderr[-200:]}'}
            
            # Get output file size
            output_size = os.path.getsize(output_path)
            
            # Calculate compression ratio
            compression_ratio = ((input_size - output_size) / input_size) * 100
            
            return {
                'success': True,
                'input_path': input_path,
                'output_path': output_path,
                'input_size_mb': round(input_size / (1024 * 1024), 2),
                'output_size_mb': round(output_size / (1024 * 1024), 2),
                'compression_ratio': round(compression_ratio, 1),
                'preset': preset
            }
            
        except subprocess.TimeoutExpired:
            return {'error': 'Compression timeout (120s)'}
        except Exception as e:
            return {'error': str(e)}
    
    def batch_compress(self, input_paths: list, preset: str = 'medium') -> Dict:
        """Compress multiple videos"""
        results = []
        total_saved = 0
        
        for path in input_paths:
            result = self.compress(path, preset=preset)
            results.append(result)
            
            if 'success' in result:
                saved_mb = result['input_size_mb'] - result['output_size_mb']
                total_saved += saved_mb
        
        successful = sum(1 for r in results if 'success' in r)
        
        return {
            'total_processed': len(input_paths),
            'successful': successful,
            'failed': len(input_paths) - successful,
            'total_saved_mb': round(total_saved, 2),
            'results': results
        }
    
    def get_compression_estimate(self, input_path: str, preset: str = 'medium') -> Dict:
        """Estimate compression results without actually compressing"""
        if not os.path.exists(input_path):
            return {'error': 'File not found'}
        
        input_size = os.path.getsize(input_path)
        
        # Rough estimates based on preset
        compression_estimates = {
            'high': 0.85,  # 15% reduction
            'medium': 0.65,  # 35% reduction
            'low': 0.45,  # 55% reduction
            'web': 0.50,  # 50% reduction
            'mobile': 0.40  # 60% reduction
        }
        
        ratio = compression_estimates.get(preset, 0.65)
        estimated_size = input_size * ratio
        estimated_saved = input_size - estimated_size
        
        return {
            'input_size_mb': round(input_size / (1024 * 1024), 2),
            'estimated_size_mb': round(estimated_size / (1024 * 1024), 2),
            'estimated_saved_mb': round(estimated_saved / (1024 * 1024), 2),
            'estimated_reduction': round((1 - ratio) * 100, 1),
            'preset': preset
        }
    
    def generate_compression_report(self, result: Dict) -> str:
        """Generate formatted compression report"""
        if 'error' in result:
            return f"❌ Error: {result['error']}"
        
        report = []
        report.append("=" * 60)
        report.append("COMPRESSION REPORT")
        report.append("=" * 60)
        report.append(f"Preset: {result['preset']}")
        report.append(f"Input: {result['input_size_mb']} MB")
        report.append(f"Output: {result['output_size_mb']} MB")
        report.append(f"Saved: {result['input_size_mb'] - result['output_size_mb']:.2f} MB")
        report.append(f"Compression: {result['compression_ratio']}%")
        report.append("")
        report.append(f"Output file: {os.path.basename(result['output_path'])}")
        report.append("=" * 60)
        
        return "\n".join(report)


# Global instance
compressor = VideoCompressor()


if __name__ == "__main__":
    print("Video Compressor Test")
    print("=" * 60)
    
    # Show available presets
    print("\nAvailable Presets:")
    for name, settings in compressor.presets.items():
        print(f"  {name:10} - {settings['description']}")
    
    # Test compression estimate
    test_file = "outputs/videos/test.mp4"
    if os.path.exists(test_file):
        print(f"\nEstimate for: {test_file}")
        estimate = compressor.get_compression_estimate(test_file, 'medium')
        print(f"  Current: {estimate['input_size_mb']} MB")
        print(f"  Estimated: {estimate['estimated_size_mb']} MB")
        print(f"  Savings: {estimate['estimated_saved_mb']} MB ({estimate['estimated_reduction']}%)")
