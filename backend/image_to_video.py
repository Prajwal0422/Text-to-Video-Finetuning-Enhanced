import cv2
import numpy as np
import imageio
from PIL import Image
import os

class MotionEngine:
    @staticmethod
    def create_video(image, output_path, duration=3, fps=24, motion_type="zoom_in"):
        """
        Applies cinematic motion transforms to a static image to create a high-quality video sequence.
        """
        img_np = np.array(image)
        h, w, _ = img_np.shape
        frames = []
        num_frames = duration * fps

        for i in range(num_frames):
            t = i / num_frames
            
            if motion_type == "zoom_in":
                # Zoom In: Scale from 1.0 to 1.15
                scale = 1.0 + (t * 0.15)
                new_w, new_h = int(w * scale), int(h * scale)
                frame = cv2.resize(img_np, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
                
                # Center Crop back to original size
                x = (new_w - w) // 2
                y = (new_h - h) // 2
                frame = frame[y:y+h, x:x+w]
                
            elif motion_type == "pan_right":
                # Pan Right: Slide window across a slightly larger scaled image
                scale = 1.1
                new_w, new_h = int(w * scale), int(h * scale)
                temp_img = cv2.resize(img_np, (new_w, new_h))
                
                max_x = new_w - w
                x = int(t * max_x)
                y = (new_h - h) // 2
                frame = temp_img[y:y+h, x:x+w]
                
            else: # Default: Subtle breathe
                scale = 1.0 + (np.sin(t * np.pi) * 0.05)
                new_w, new_h = int(w * scale), int(h * scale)
                frame = cv2.resize(img_np, (new_w, new_h))
                x = (new_w - w) // 2
                y = (new_h - h) // 2
                frame = frame[y:y+h, x:x+w]

            frames.append(frame)

        # Save as MP4
        imageio.mimsave(output_path, frames, fps=fps, quality=9)
        return output_path
