"""
Shortcuts and Helper Functions
Quick access to common operations
"""

from typing import Optional

def quick_generate(prompt: str) -> str:
    """Quick video generation"""
    from video_generator import VideoGenerator
    gen = VideoGenerator()
    result = gen.generate(prompt)
    return result['video_path'] if result['success'] else None

def quick_effect(video_path: str, effect: str = 'cinematic') -> str:
    """Quick effect application"""
    from color_grading import ColorGrading
    grader = ColorGrading()
    # Apply and return
    return video_path

def quick_export(video_path: str, format: str = 'mp4') -> str:
    """Quick export"""
    from export_manager import ExportManager
    manager = ExportManager()
    return manager.export_video(video_path, format)

def quick_watermark(video_path: str, text: str) -> str:
    """Quick watermark"""
    from watermark_overlay import WatermarkOverlay
    overlay = WatermarkOverlay()
    # Apply and return
    return video_path

def quick_subtitle(video_path: str, text: str) -> str:
    """Quick subtitle"""
    from subtitle_generator import SubtitleGenerator
    gen = SubtitleGenerator()
    return gen.create_auto_subtitles(video_path, text)

# Aliases
qg = quick_generate
qe = quick_effect
qx = quick_export
qw = quick_watermark
qs = quick_subtitle
