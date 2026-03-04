"""
Quality Analysis
Analyze video quality and complexity
"""

import cv2
import numpy as np
from typing import Dict, List


class QualityAnalyzer:
    """Analyze video quality metrics"""
    
    @staticmethod
    def analyze_frame_complexity(frame: np.ndarray) -> float:
        """
        Analyze frame complexity (0-1)
        
        Args:
            frame: Input frame
            
        Returns:
            Complexity score (0=simple, 1=complex)
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Calculate edge density
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / edges.size
        
        # Calculate texture complexity using Laplacian variance
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        texture_variance = np.var(laplacian)
        texture_score = min(texture_variance / 1000, 1.0)
        
        # Combine metrics
        complexity = (edge_density * 0.6 + texture_score * 0.4)
        
        return min(complexity, 1.0)
    
    @staticmethod
    def analyze_motion_intensity(frame1: np.ndarray, frame2: np.ndarray) -> float:
        """
        Analyze motion intensity between two frames
        
        Args:
            frame1: First frame
            frame2: Second frame
            
        Returns:
            Motion intensity (0-1)
        """
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        
        # Calculate frame difference
        diff = np.abs(gray1.astype(float) - gray2.astype(float))
        motion_score = np.mean(diff) / 255.0
        
        return min(motion_score, 1.0)
    
    @staticmethod
    def analyze_sharpness(frame: np.ndarray) -> float:
        """
        Analyze frame sharpness
        
        Args:
            frame: Input frame
            
        Returns:
            Sharpness score (higher = sharper)
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        sharpness = np.var(laplacian)
        
        return sharpness
    
    @staticmethod
    def analyze_brightness(frame: np.ndarray) -> Dict:
        """
        Analyze frame brightness
        
        Args:
            frame: Input frame
            
        Returns:
            Dictionary with brightness metrics
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        return {
            "mean": float(np.mean(gray)),
            "median": float(np.median(gray)),
            "std": float(np.std(gray)),
            "min": int(np.min(gray)),
            "max": int(np.max(gray))
        }
    
    @staticmethod
    def analyze_color_distribution(frame: np.ndarray) -> Dict:
        """
        Analyze color distribution
        
        Args:
            frame: Input frame
            
        Returns:
            Dictionary with color metrics
        """
        # Calculate histograms for each channel
        b_hist = cv2.calcHist([frame], [0], None, [256], [0, 256])
        g_hist = cv2.calcHist([frame], [1], None, [256], [0, 256])
        r_hist = cv2.calcHist([frame], [2], None, [256], [0, 256])
        
        # Calculate color variance
        b_var = np.var(frame[:, :, 0])
        g_var = np.var(frame[:, :, 1])
        r_var = np.var(frame[:, :, 2])
        
        return {
            "blue_variance": float(b_var),
            "green_variance": float(g_var),
            "red_variance": float(r_var),
            "total_variance": float(b_var + g_var + r_var)
        }
    
    @staticmethod
    def analyze_sequence(frames: List[np.ndarray]) -> Dict:
        """
        Analyze entire video sequence
        
        Args:
            frames: List of frames
            
        Returns:
            Dictionary with sequence metrics
        """
        if len(frames) == 0:
            return {}
        
        # Analyze complexity
        complexities = [QualityAnalyzer.analyze_frame_complexity(f) for f in frames]
        
        # Analyze motion
        motion_scores = []
        for i in range(len(frames) - 1):
            motion = QualityAnalyzer.analyze_motion_intensity(frames[i], frames[i + 1])
            motion_scores.append(motion)
        
        # Analyze sharpness
        sharpness_scores = [QualityAnalyzer.analyze_sharpness(f) for f in frames]
        
        return {
            "num_frames": len(frames),
            "avg_complexity": float(np.mean(complexities)),
            "max_complexity": float(np.max(complexities)),
            "avg_motion": float(np.mean(motion_scores)) if motion_scores else 0.0,
            "max_motion": float(np.max(motion_scores)) if motion_scores else 0.0,
            "avg_sharpness": float(np.mean(sharpness_scores)),
            "min_sharpness": float(np.min(sharpness_scores))
        }
    
    @staticmethod
    def recommend_settings(frame: np.ndarray) -> Dict:
        """
        Recommend optimal settings based on frame analysis
        
        Args:
            frame: Sample frame
            
        Returns:
            Dictionary with recommended settings
        """
        complexity = QualityAnalyzer.analyze_frame_complexity(frame)
        brightness = QualityAnalyzer.analyze_brightness(frame)
        
        # Determine quality mode
        if complexity > 0.7:
            quality_mode = "quality"
            fps = 60
        elif complexity > 0.4:
            quality_mode = "balanced"
            fps = 30
        else:
            quality_mode = "fast"
            fps = 24
        
        # Determine if color grading needed
        needs_grading = brightness["mean"] < 100 or brightness["mean"] > 180
        
        return {
            "quality_mode": quality_mode,
            "recommended_fps": fps,
            "complexity_score": complexity,
            "needs_color_grading": needs_grading,
            "brightness_ok": 100 <= brightness["mean"] <= 180
        }
