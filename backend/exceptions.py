"""Custom Exceptions for Video Generation"""

class VideoGenerationError(Exception):
    """Base exception for video generation errors"""
    pass

class GPUNotAvailableError(VideoGenerationError):
    """Raised when GPU is required but not available"""
    pass

class InvalidMotionTypeError(VideoGenerationError):
    """Raised when invalid motion type is specified"""
    pass

class CacheError(VideoGenerationError):
    """Raised when cache operations fail"""
    pass

class CompressionError(VideoGenerationError):
    """Raised when video compression fails"""
    pass
