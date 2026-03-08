"""
NEXUS VISION - Custom Exceptions
Centralized exception handling
"""

class NexusVisionException(Exception):
    """Base exception for NEXUS VISION"""
    pass

class VideoGenerationError(NexusVisionException):
    """Raised when video generation fails"""
    pass

class ClipFetchError(NexusVisionException):
    """Raised when clip fetching fails"""
    pass

class ScriptGenerationError(NexusVisionException):
    """Raised when script generation fails"""
    pass

class VideoEditingError(NexusVisionException):
    """Raised when video editing fails"""
    pass

class APIKeyError(NexusVisionException):
    """Raised when API key is invalid or missing"""
    pass

class ConfigurationError(NexusVisionException):
    """Raised when configuration is invalid"""
    pass

class CacheError(NexusVisionException):
    """Raised when cache operations fail"""
    pass

class ValidationError(NexusVisionException):
    """Raised when input validation fails"""
    pass
