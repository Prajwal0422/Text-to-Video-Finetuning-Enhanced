"""Input Validation Functions"""

from exceptions import InvalidMotionTypeError
from constants import *

def validate_fps(fps):
    """Validate FPS value"""
    if not isinstance(fps, int) or fps < 1 or fps > 120:
        raise ValueError(f"Invalid FPS: {fps}. Must be between 1 and 120")
    return fps

def validate_quality(quality):
    """Validate quality preset"""
    valid = [QUALITY_FAST, QUALITY_BALANCED, QUALITY_HIGH]
    if quality not in valid:
        raise ValueError(f"Invalid quality: {quality}. Must be one of {valid}")
    return quality

def validate_motion_type(motion_type):
    """Validate motion type"""
    valid = [MOTION_ZOOM_IN, MOTION_ZOOM_OUT, MOTION_PAN_RIGHT, 
             MOTION_PAN_LEFT, MOTION_KEN_BURNS]
    if motion_type not in valid:
        raise InvalidMotionTypeError(f"Invalid motion: {motion_type}")
    return motion_type

def validate_resolution(resolution):
    """Validate resolution tuple"""
    if not isinstance(resolution, tuple) or len(resolution) != 2:
        raise ValueError("Resolution must be a tuple of (width, height)")
    w, h = resolution
    if w < 1 or h < 1:
        raise ValueError("Resolution dimensions must be positive")
    return resolution
