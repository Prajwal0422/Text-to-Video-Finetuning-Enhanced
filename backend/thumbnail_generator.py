"""
Thumbnail Generator
Generates attractive thumbnails from video files
"""

import os
from typing import Optional, List
from moviepy import VideoFileClip
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

class ThumbnailGenerator:
    """Generates thumbnails from videos"""
    
    def __init__(self, output_dir: str = "outputs/thumbnails"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def extract_frame(
        self,
        video_path: str,
        timestamp: float = None
    ) -> Image.Image:
        """
        Extract a frame from video
        
        Args:
            video_path: Path to video file
            timestamp: Time in seconds (None = middle of video)
        
        Returns:
            PIL Image
        """
        clip = VideoFileClip(video_path)
        
        if timestamp is None:
            timestamp = clip.duration / 2  # Middle frame
        
        # Get frame
        frame = clip.get_frame(timestamp)
        clip.close()
        
        # Convert to PIL Image
        return Image.fromarray(frame)
    
    def enhance_image(self, image: Image.Image) -> Image.Image:
        """Enhance image quality"""
        # Increase contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.2)
        
        # Increase saturation
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.1)
        
        # Slight sharpening
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(1.1)
        
        return image
    
    def add_text_overlay(
        self,
        image: Image.Image,
        text: str,
        position: str = 'bottom'
    ) -> Image.Image:
        """
        Add text overlay to image
        
        Args:
            image: PIL Image
            text: Text to overlay
            position: 'top', 'bottom', or 'center'
        
        Returns:
            Image with text overlay
        """
        # Create a copy
        img = image.copy()
        draw = ImageDraw.Draw(img)
        
        # Calculate text size and position
        width, height = img.size
        
        # Try to use a nice font, fallback to default
        try:
            font_size = int(height * 0.06)  # 6% of image height
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Get text bounding box
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Calculate position
        x = (width - text_width) // 2
        
        if position == 'top':
            y = int(height * 0.05)
        elif position == 'center':
            y = (height - text_height) // 2
        else:  # bottom
            y = int(height * 0.85)
        
        # Draw semi-transparent background
        padding = 20
        bg_bbox = [
            x - padding,
            y - padding,
            x + text_width + padding,
            y + text_height + padding
        ]
        draw.rectangle(bg_bbox, fill=(0, 0, 0, 180))
        
        # Draw text with outline for better visibility
        outline_color = (0, 0, 0)
        text_color = (255, 255, 255)
        
        # Draw outline
        for adj_x in [-2, 0, 2]:
            for adj_y in [-2, 0, 2]:
                draw.text((x + adj_x, y + adj_y), text, font=font, fill=outline_color)
        
        # Draw main text
        draw.text((x, y), text, font=font, fill=text_color)
        
        return img
    
    def create_thumbnail(
        self,
        video_path: str,
        output_filename: Optional[str] = None,
        timestamp: Optional[float] = None,
        text: Optional[str] = None,
        size: tuple = (1280, 720),
        enhance: bool = True
    ) -> str:
        """
        Create thumbnail from video
        
        Args:
            video_path: Path to video file
            output_filename: Output filename (auto-generated if None)
            timestamp: Frame timestamp (None = middle)
            text: Optional text overlay
            size: Thumbnail size (width, height)
            enhance: Apply image enhancements
        
        Returns:
            Path to generated thumbnail
        """
        # Extract frame
        image = self.extract_frame(video_path, timestamp)
        
        # Resize
        image = image.resize(size, Image.Resampling.LANCZOS)
        
        # Enhance
        if enhance:
            image = self.enhance_image(image)
        
        # Add text overlay
        if text:
            image = self.add_text_overlay(image, text)
        
        # Generate output filename
        if not output_filename:
            video_basename = os.path.splitext(os.path.basename(video_path))[0]
            output_filename = f"thumb_{video_basename}.jpg"
        
        output_path = os.path.join(self.output_dir, output_filename)
        
        # Save
        image.save(output_path, 'JPEG', quality=90, optimize=True)
        
        return output_path
    
    def create_multiple_thumbnails(
        self,
        video_path: str,
        count: int = 3
    ) -> List[str]:
        """
        Create multiple thumbnails at different timestamps
        
        Args:
            video_path: Path to video file
            count: Number of thumbnails to generate
        
        Returns:
            List of thumbnail paths
        """
        clip = VideoFileClip(video_path)
        duration = clip.duration
        clip.close()
        
        thumbnails = []
        
        for i in range(count):
            # Distribute timestamps evenly
            timestamp = (duration / (count + 1)) * (i + 1)
            
            output_filename = f"thumb_{os.path.splitext(os.path.basename(video_path))[0]}_{i+1}.jpg"
            
            thumb_path = self.create_thumbnail(
                video_path,
                output_filename=output_filename,
                timestamp=timestamp
            )
            
            thumbnails.append(thumb_path)
        
        return thumbnails


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("THUMBNAIL GENERATOR - TEST")
    print("=" * 60)
    
    generator = ThumbnailGenerator()
    
    # Test with a video file (if exists)
    test_video = "outputs/videos/video_273973db.mp4"
    
    if os.path.exists(test_video):
        print(f"\nGenerating thumbnail from: {test_video}")
        
        thumb_path = generator.create_thumbnail(
            test_video,
            text="Ocean Waves",
            enhance=True
        )
        
        print(f"✅ Thumbnail created: {thumb_path}")
        
        # Create multiple thumbnails
        print("\nGenerating multiple thumbnails...")
        thumbs = generator.create_multiple_thumbnails(test_video, count=3)
        
        for i, thumb in enumerate(thumbs, 1):
            print(f"  {i}. {thumb}")
    else:
        print(f"\n⚠️  Test video not found: {test_video}")
        print("   Generate a video first to test thumbnail creation")
