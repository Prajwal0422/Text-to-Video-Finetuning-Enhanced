"""
Scene Detector
Detects scene changes and analyzes video content
"""

import cv2
import numpy as np
from typing import List, Dict, Tuple
import os

class SceneDetector:
    """Detects scenes and analyzes video content"""
    
    def __init__(self, threshold: float = 30.0):
        self.threshold = threshold
    
    def detect_scenes(self, video_path: str) -> List[Dict]:
        """
        Detect scene changes in video
        
        Args:
            video_path: Path to video file
        
        Returns:
            List of scene information
        """
        cap = cv2.VideoCapture(video_path)
        
        scenes = []
        frame_count = 0
        prev_frame = None
        scene_start = 0
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            if prev_frame is not None:
                # Calculate difference
                diff = cv2.absdiff(prev_frame, gray)
                mean_diff = np.mean(diff)
                
                # Scene change detected
                if mean_diff > self.threshold:
                    scene_end = frame_count
                    scenes.append({
                        'start_frame': scene_start,
                        'end_frame': scene_end,
                        'start_time': scene_start / fps,
                        'end_time': scene_end / fps,
                        'duration': (scene_end - scene_start) / fps
                    })
                    scene_start = frame_count
            
            prev_frame = gray
            frame_count += 1
        
        # Add final scene
        if scene_start < frame_count:
            scenes.append({
                'start_frame': scene_start,
                'end_frame': frame_count,
                'start_time': scene_start / fps,
                'end_time': frame_count / fps,
                'duration': (frame_count - scene_start) / fps
            })
        
        cap.release()
        
        return scenes
    
    def analyze_brightness(self, video_path: str) -> Dict:
        """Analyze video brightness"""
        cap = cv2.VideoCapture(video_path)
        
        brightness_values = []
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            brightness = np.mean(gray)
            brightness_values.append(brightness)
        
        cap.release()
        
        return {
            'avg_brightness': np.mean(brightness_values),
            'min_brightness': np.min(brightness_values),
            'max_brightness': np.max(brightness_values),
            'std_brightness': np.std(brightness_values)
        }
    
    def detect_motion(self, video_path: str) -> Dict:
        """Detect motion intensity in video"""
        cap = cv2.VideoCapture(video_path)
        
        motion_scores = []
        prev_frame = None
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            if prev_frame is not None:
                flow = cv2.calcOpticalFlowFarneback(
                    prev_frame, gray, None,
                    0.5, 3, 15, 3, 5, 1.2, 0
                )
                
                magnitude = np.sqrt(flow[..., 0]**2 + flow[..., 1]**2)
                motion_score = np.mean(magnitude)
                motion_scores.append(motion_score)
            
            prev_frame = gray
        
        cap.release()
        
        return {
            'avg_motion': np.mean(motion_scores) if motion_scores else 0,
            'max_motion': np.max(motion_scores) if motion_scores else 0,
            'motion_intensity': 'high' if np.mean(motion_scores) > 5 else 'low'
        }
    
    def extract_keyframes(
        self,
        video_path: str,
        num_frames: int = 5
    ) -> List[str]:
        """Extract key frames from video"""
        cap = cv2.VideoCapture(video_path)
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_indices = np.linspace(0, total_frames - 1, num_frames, dtype=int)
        
        keyframes = []
        output_dir = "outputs/keyframes"
        os.makedirs(output_dir, exist_ok=True)
        
        for idx in frame_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ret, frame = cap.read()
            
            if ret:
                filename = f"keyframe_{idx}.jpg"
                filepath = os.path.join(output_dir, filename)
                cv2.imwrite(filepath, frame)
                keyframes.append(filepath)
        
        cap.release()
        
        return keyframes


if __name__ == "__main__":
    print("Scene Detector - Ready for video analysis")
