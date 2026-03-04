"""
Speed Optimization Engine
Multi-threaded processing, caching, and performance tuning
"""

import cv2
import numpy as np
from typing import List, Callable, Any
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from functools import lru_cache
import hashlib
import pickle
import os


class MultiThreadProcessor:
    """Parallel processing for video operations"""
    
    def __init__(self, max_workers: int = None):
        self.max_workers = max_workers or os.cpu_count()
    
    def process_frames_parallel(self, frames: List[np.ndarray], 
                               process_func: Callable, 
                               use_processes: bool = False) -> List[np.ndarray]:
        """Process frames in parallel using threads or processes"""
        executor_class = ProcessPoolExecutor if use_processes else ThreadPoolExecutor
        
        with executor_class(max_workers=self.max_workers) as executor:
            results = list(executor.map(process_func, frames))
        
        return results
    
    def process_frame_pairs_parallel(self, frame_pairs: List[tuple],
                                    process_func: Callable) -> List[Any]:
        """Process frame pairs in parallel"""
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            results = list(executor.map(lambda p: process_func(*p), frame_pairs))
        
        return results


class CacheManager:
    """Intelligent caching for repeated operations"""
    
    def __init__(self, cache_dir: str = ".cache/video"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def get_cache_key(self, data: Any) -> str:
        """Generate cache key from data"""
        serialized = pickle.dumps(data)
        return hashlib.md5(serialized).hexdigest()
    
    def cache_frame_operation(self, frame: np.ndarray, operation: str,
                             params: dict) -> str:
        """Cache processed frame"""
        cache_key = self.get_cache_key((frame.tobytes(), operation, params))
        cache_path = os.path.join(self.cache_dir, f"{cache_key}.npy")
        return cache_path
    
    def load_cached_frame(self, cache_path: str) -> np.ndarray:
        """Load cached frame"""
        if os.path.exists(cache_path):
            return np.load(cache_path)
        return None
    
    def save_cached_frame(self, frame: np.ndarray, cache_path: str):
        """Save frame to cache"""
        np.save(cache_path, frame)


class MemoryOptimizer:
    """Memory management for large video operations"""
    
    @staticmethod
    def estimate_memory_usage(frame_shape: tuple, num_frames: int, 
                             dtype=np.uint8) -> float:
        """Estimate memory usage in MB"""
        bytes_per_pixel = np.dtype(dtype).itemsize
        total_bytes = np.prod(frame_shape) * num_frames * bytes_per_pixel
        return total_bytes / (1024 * 1024)
    
    @staticmethod
    def should_use_streaming(num_frames: int, frame_shape: tuple,
                           memory_limit_mb: float = 1000) -> bool:
        """Determine if streaming processing is needed"""
        estimated_mb = MemoryOptimizer.estimate_memory_usage(
            frame_shape, num_frames
        )
        return estimated_mb > memory_limit_mb
    
    @staticmethod
    def process_in_chunks(frames: List[np.ndarray], 
                         process_func: Callable,
                         chunk_size: int = 50) -> List[np.ndarray]:
        """Process frames in memory-efficient chunks"""
        results = []
        for i in range(0, len(frames), chunk_size):
            chunk = frames[i:i + chunk_size]
            processed = [process_func(frame) for frame in chunk]
            results.extend(processed)
            # Clear chunk from memory
            del chunk
        return results


class CompressionOptimizer:
    """Video compression optimization"""
    
    @staticmethod
    def get_optimal_codec(quality: str = "balanced") -> tuple:
        """Get optimal codec and parameters"""
        codecs = {
            "fast": ("mp4v", 20),  # MPEG-4, lower quality
            "balanced": ("avc1", 23),  # H.264, balanced
            "quality": ("avc1", 18),  # H.264, high quality
            "max": ("hev1", 20)  # H.265, best compression
        }
        
        codec, crf = codecs.get(quality, codecs["balanced"])
        return cv2.VideoWriter_fourcc(*codec), crf
    
    @staticmethod
    def optimize_bitrate(resolution: tuple, fps: int, quality: str) -> int:
        """Calculate optimal bitrate"""
        width, height = resolution
        pixels = width * height
        
        # Base bitrate per megapixel
        base_rates = {
            "fast": 2000,
            "balanced": 4000,
            "quality": 8000,
            "max": 12000
        }
        
        base = base_rates.get(quality, 4000)
        megapixels = pixels / (1920 * 1080)
        
        return int(base * megapixels * (fps / 30))


class GPUAccelerator:
    """GPU acceleration utilities"""
    
    @staticmethod
    def is_gpu_available() -> bool:
        """Check if GPU acceleration is available"""
        try:
            return cv2.cuda.getCudaEnabledDeviceCount() > 0
        except:
            return False
    
    @staticmethod
    def upload_to_gpu(frame: np.ndarray):
        """Upload frame to GPU memory"""
        if GPUAccelerator.is_gpu_available():
            return cv2.cuda_GpuMat(frame)
        return frame
    
    @staticmethod
    def download_from_gpu(gpu_frame):
        """Download frame from GPU memory"""
        if GPUAccelerator.is_gpu_available() and hasattr(gpu_frame, 'download'):
            return gpu_frame.download()
        return gpu_frame
    
    @staticmethod
    def resize_gpu(frame: np.ndarray, size: tuple) -> np.ndarray:
        """GPU-accelerated resize"""
        if GPUAccelerator.is_gpu_available():
            gpu_frame = cv2.cuda_GpuMat(frame)
            gpu_resized = cv2.cuda.resize(gpu_frame, size)
            return gpu_resized.download()
        return cv2.resize(frame, size)


class AdaptiveQualityManager:
    """Dynamic quality adjustment based on content"""
    
    @staticmethod
    def analyze_frame_complexity(frame: np.ndarray) -> float:
        """Analyze frame complexity (0-1)"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Calculate edge density
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / edges.size
        
        # Calculate texture complexity
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        texture_variance = np.var(laplacian)
        
        # Normalize and combine
        complexity = (edge_density * 0.6 + 
                     min(texture_variance / 1000, 1.0) * 0.4)
        
        return min(complexity, 1.0)
    
    @staticmethod
    def adjust_quality_settings(complexity: float, base_quality: str) -> dict:
        """Adjust quality settings based on complexity"""
        quality_map = {
            "fast": {"fps": 24, "resolution_scale": 0.8},
            "balanced": {"fps": 30, "resolution_scale": 1.0},
            "quality": {"fps": 60, "resolution_scale": 1.0}
        }
        
        settings = quality_map.get(base_quality, quality_map["balanced"]).copy()
        
        # Adjust for high complexity
        if complexity > 0.7:
            settings["fps"] = min(settings["fps"] + 6, 60)
        elif complexity < 0.3:
            settings["fps"] = max(settings["fps"] - 6, 24)
            settings["resolution_scale"] *= 0.9
        
        return settings


class PreprocessingPipeline:
    """Optimized preprocessing pipeline"""
    
    @staticmethod
    def fast_normalize(frame: np.ndarray) -> np.ndarray:
        """Fast frame normalization"""
        # Use lookup table for faster processing
        lut = np.arange(256, dtype=np.uint8)
        return cv2.LUT(frame, lut)
    
    @staticmethod
    def fast_denoise(frame: np.ndarray, strength: int = 3) -> np.ndarray:
        """Fast denoising"""
        return cv2.fastNlMeansDenoisingColored(frame, None, strength, strength, 7, 21)
    
    @staticmethod
    def fast_sharpen(frame: np.ndarray, amount: float = 1.0) -> np.ndarray:
        """Fast sharpening"""
        kernel = np.array([[-1, -1, -1],
                          [-1, 9 + amount, -1],
                          [-1, -1, -1]]) / (1 + amount)
        return cv2.filter2D(frame, -1, kernel)
    
    @staticmethod
    def batch_preprocess(frames: List[np.ndarray], 
                        operations: List[str]) -> List[np.ndarray]:
        """Batch preprocessing with multiple operations"""
        processor = MultiThreadProcessor()
        
        def apply_operations(frame):
            result = frame
            for op in operations:
                if op == "normalize":
                    result = PreprocessingPipeline.fast_normalize(result)
                elif op == "denoise":
                    result = PreprocessingPipeline.fast_denoise(result)
                elif op == "sharpen":
                    result = PreprocessingPipeline.fast_sharpen(result)
            return result
        
        return processor.process_frames_parallel(frames, apply_operations)


class PerformanceProfiler:
    """Performance monitoring and optimization suggestions"""
    
    def __init__(self):
        self.timings = {}
    
    def profile_operation(self, operation_name: str, duration: float):
        """Record operation timing"""
        if operation_name not in self.timings:
            self.timings[operation_name] = []
        self.timings[operation_name].append(duration)
    
    def get_bottlenecks(self) -> List[tuple]:
        """Identify performance bottlenecks"""
        avg_timings = {
            name: np.mean(times) 
            for name, times in self.timings.items()
        }
        
        sorted_ops = sorted(avg_timings.items(), 
                          key=lambda x: x[1], reverse=True)
        return sorted_ops[:3]
    
    def suggest_optimizations(self) -> List[str]:
        """Suggest performance optimizations"""
        suggestions = []
        bottlenecks = self.get_bottlenecks()
        
        for op_name, avg_time in bottlenecks:
            if "resize" in op_name.lower() and avg_time > 0.1:
                suggestions.append(f"Consider GPU acceleration for {op_name}")
            elif "process" in op_name.lower() and avg_time > 0.5:
                suggestions.append(f"Use parallel processing for {op_name}")
            elif avg_time > 1.0:
                suggestions.append(f"Optimize {op_name} - taking {avg_time:.2f}s")
        
        return suggestions
