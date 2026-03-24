"""
Watermark Overlay System
Add watermarks and logos to videos
"""

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from typing import Optional, Tuple
import os

class WatermarkOverlay:
    """Add watermarks to videos"""
    
    POSITIONS = {
        'top-left': (0.05, 0.05),
        'top-right': (0.95, 0.05),
        'bottom-left': (0.05, 0.95),
        'bottom-right': (0.95, 0.95),
        'center': (0.5, 0.5)
    }
    
    def __init__(self):
        self.watermarks_dir = "watermarks"
        os.makedirs(self.watermarks_dir, exist_ok=True)
    
    def add_text_watermark(
        self,
        frame: np.ndarray,
        text: str,
        position: str = 'bottom-right',
        font_size: int = 30,
        opacity: float = 0.5,
        color: Tuple[int, int, int] = (255, 255, 255)
    ) -> np.ndarray:
        """Add text watermark to frame"""
        # Convert to PIL Image
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        # Create transparent overlay
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Load font
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Get text size
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Calculate position
        pos_x, pos_y = self.POSITIONS[position]
        x = int(pos_x * img.width - (text_width if pos_x > 0.5 else 0))
        y = int(pos_y * img.height - (text_height if pos_y > 0.5 else 0))
        
        # Draw text with opacity
        text_color = color + (int(255 * opacity),)
        draw.text((x, y), text, font=font, fill=text_color)
        
        # Composite
        img = img.convert('RGBA')
        img = Image.alpha_composite(img, overlay)
        img = img.convert('RGB')
        
        # Convert back to OpenCV
        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    
    def add_logo_watermark(
        self,
        frame: np.ndarray,
        logo_path: str,
        position: str = 'bottom-right',
        scale: float = 0.1,
        opacity: float = 0.7
    ) -> np.ndarray:
        """Add logo watermark to frame"""
        if not os.path.exists(logo_path):
            raise FileNotFoundError(f"Logo not found: {logo_path}")
        
        # Load logo
        logo = cv2.imread(logo_path, cv2.IMREAD_UNCHANGED)
        
        # Resize logo
        h, w = frame.shape[:2]
        logo_h = int(h * scale)
        logo_w = int(logo.shape[1] * (logo_h / logo.shape[0]))
        logo = cv2.resize(logo, (logo_w, logo_h))
        
        # Calculate position
        pos_x, pos_y = self.POSITIONS[position]
        x = int(pos_x * w - (logo_w if pos_x > 0.5 else 0))
        y = int(pos_y * h - (logo_h if pos_y > 0.5 else 0))
        
        # Ensure logo fits
        x = max(0, min(x, w - logo_w))
        y = max(0, min(y, h - logo_h))
        
        # Apply logo with opacity
        if logo.shape[2] == 4:  # Has alpha channel
            alpha = logo[:, :, 3] / 255.0 * opacity
            alpha = np.dstack([alpha] * 3)
            
            roi = frame[y:y+logo_h, x:x+logo_w]
            logo_rgb = logo[:, :, :3]
            
            blended = (logo_rgb * alpha + roi * (1 - alpha)).astype(np.uint8)
            frame[y:y+logo_h, x:x+logo_w] = blended
        else:
            # No alpha channel, simple overlay
            frame[y:y+logo_h, x:x+logo_w] = logo
        
        return frame
    
    def create_text_logo(
        self,
        text: str,
        output_path: str,
        size: Tuple[int, int] = (200, 100),
        font_size: int = 40,
        bg_color: Tuple[int, int, int, int] = (0, 0, 0, 0),
        text_color: Tuple[int, int, int, int] = (255, 255, 255, 255)
    ) -> str:
        """Create a text-based logo"""
        img = Image.new('RGBA', size, bg_color)
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Center text
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (size[0] - text_width) // 2
        y = (size[1] - text_height) // 2
        
        draw.text((x, y), text, font=font, fill=text_color)
        
        img.save(output_path)
        return output_path
    
    def add_timestamp(
        self,
        frame: np.ndarray,
        timestamp: str,
        position: str = 'top-right'
    ) -> np.ndarray:
        """Add timestamp to frame"""
        return self.add_text_watermark(
            frame,
            timestamp,
            position=position,
            font_size=20,
            opacity=0.7
        )


if __name__ == "__main__":
    overlay = WatermarkOverlay()
    print("Watermark Overlay System Ready")
    print(f"Available positions: {list(overlay.POSITIONS.keys())}")
