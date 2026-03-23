"""
Export Manager
Manages video exports in different formats and qualities
"""

import os
import subprocess
from typing import Dict, Optional, List
from dataclasses import dataclass
import imageio_ffmpeg

@dataclass
class ExportProfile:
    """Video export profile"""
    name: str
    width: int
    height: int
    fps: int
    bitrate: str
    codec: str
    format: str
    audio: bool = False

class ExportManager:
    """Manages video exports with different profiles"""
    
    # Predefined export profiles
    PROFILES = {
        'web_low': ExportProfile(
            name='Web Low Quality',
            width=480,
            height=270,
            fps=24,
            bitrate='500k',
            codec='libx264',
            format='mp4',
            audio=False
        ),
        'web_medium': ExportProfile(
            name='Web Medium Quality',
            width=640,
            height=360,
            fps=24,
            bitrate='1000k',
            codec='libx264',
            format='mp4',
            audio=False
        ),
        'web_high': ExportProfile(
            name='Web High Quality',
            width=1280,
            height=720,
            fps=30,
            bitrate='2500k',
            codec='libx264',
            format='mp4',
            audio=False
        ),
        'social_instagram': ExportProfile(
            name='Instagram',
            width=1080,
            height=1080,
            fps=30,
            bitrate='3500k',
            codec='libx264',
            format='mp4',
            audio=False
        ),
        'social_tiktok': ExportProfile(
            name='TikTok',
            width=1080,
            height=1920,
            fps=30,
            bitrate='4000k',
            codec='libx264',
            format='mp4',
            audio=False
        ),
        'gif': ExportProfile(
            name='Animated GIF',
            width=480,
            height=270,
            fps=15,
            bitrate='',
            codec='gif',
            format='gif',
            audio=False
        )
    }
    
    def __init__(self, output_dir: str = "outputs/exports"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        try:
            self.ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
        except Exception as e:
            raise RuntimeError(f"FFmpeg not available: {e}")
    
    def export_video(
        self,
        input_path: str,
        profile_name: str,
        output_filename: Optional[str] = None
    ) -> str:
        """
        Export video with specified profile
        
        Args:
            input_path: Path to input video
            profile_name: Name of export profile
            output_filename: Optional output filename
        
        Returns:
            Path to exported video
        """
        if profile_name not in self.PROFILES:
            raise ValueError(f"Unknown profile: {profile_name}")
        
        profile = self.PROFILES[profile_name]
        
        # Generate output filename
        if not output_filename:
            basename = os.path.splitext(os.path.basename(input_path))[0]
            output_filename = f"{basename}_{profile_name}.{profile.format}"
        
        output_path = os.path.join(self.output_dir, output_filename)
        
        # Build FFmpeg command
        if profile.format == 'gif':
            cmd = self._build_gif_command(input_path, output_path, profile)
        else:
            cmd = self._build_video_command(input_path, output_path, profile)
        
        # Execute
        print(f"Exporting with profile '{profile.name}'...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise RuntimeError(f"Export failed: {result.stderr[-200:]}")
        
        # Verify output
        if not os.path.exists(output_path):
            raise RuntimeError("Output file not created")
        
        file_size = os.path.getsize(output_path)
        print(f"✅ Exported: {output_path} ({file_size / 1024 / 1024:.2f} MB)")
        
        return output_path
    
    def _build_video_command(
        self,
        input_path: str,
        output_path: str,
        profile: ExportProfile
    ) -> List[str]:
        """Build FFmpeg command for video export"""
        cmd = [
            self.ffmpeg_path,
            '-y',  # Overwrite
            '-i', input_path,
            '-vf', f'scale={profile.width}:{profile.height}',
            '-r', str(profile.fps),
            '-c:v', profile.codec,
            '-b:v', profile.bitrate,
            '-preset', 'medium',
            '-movflags', '+faststart'  # Web optimization
        ]
        
        if not profile.audio:
            cmd.append('-an')
        
        cmd.append(output_path)
        
        return cmd
    
    def _build_gif_command(
        self,
        input_path: str,
        output_path: str,
        profile: ExportProfile
    ) -> List[str]:
        """Build FFmpeg command for GIF export"""
        cmd = [
            self.ffmpeg_path,
            '-y',
            '-i', input_path,
            '-vf', f'fps={profile.fps},scale={profile.width}:{profile.height}:flags=lanczos',
            '-loop', '0',
            output_path
        ]
        
        return cmd
    
    def export_multiple(
        self,
        input_path: str,
        profile_names: List[str]
    ) -> Dict[str, str]:
        """
        Export video in multiple profiles
        
        Args:
            input_path: Path to input video
            profile_names: List of profile names
        
        Returns:
            Dictionary mapping profile names to output paths
        """
        results = {}
        
        for profile_name in profile_names:
            try:
                output_path = self.export_video(input_path, profile_name)
                results[profile_name] = output_path
            except Exception as e:
                print(f"❌ Failed to export {profile_name}: {e}")
                results[profile_name] = None
        
        return results
    
    def get_available_profiles(self) -> List[Dict]:
        """Get list of available export profiles"""
        return [
            {
                'id': key,
                'name': profile.name,
                'resolution': f"{profile.width}x{profile.height}",
                'fps': profile.fps,
                'format': profile.format
            }
            for key, profile in self.PROFILES.items()
        ]


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("EXPORT MANAGER - TEST")
    print("=" * 60)
    
    manager = ExportManager()
    
    # Show available profiles
    print("\nAvailable Export Profiles:")
    for profile in manager.get_available_profiles():
        print(f"  - {profile['id']}: {profile['name']} ({profile['resolution']} @ {profile['fps']}fps)")
    
    # Test export (if video exists)
    test_video = "outputs/videos/video_273973db.mp4"
    
    if os.path.exists(test_video):
        print(f"\nExporting: {test_video}")
        
        # Export to multiple formats
        profiles = ['web_low', 'web_medium', 'gif']
        results = manager.export_multiple(test_video, profiles)
        
        print("\nExport Results:")
        for profile, path in results.items():
            if path:
                size = os.path.getsize(path) / 1024 / 1024
                print(f"  ✅ {profile}: {path} ({size:.2f} MB)")
            else:
                print(f"  ❌ {profile}: Failed")
    else:
        print(f"\n⚠️  Test video not found: {test_video}")
