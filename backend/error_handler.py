"""
Error Handler
Centralized error handling and recovery
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class VideoGenerationError(Exception):
    """Base exception for video generation errors"""
    pass

class APIError(VideoGenerationError):
    """API related errors"""
    pass

class ClipFetchError(VideoGenerationError):
    """Clip fetching errors"""
    pass

class VideoEditError(VideoGenerationError):
    """Video editing errors"""
    pass

class TimeoutError(VideoGenerationError):
    """Timeout errors"""
    pass

def handle_api_error(error: Exception) -> Dict[str, Any]:
    """Handle API errors"""
    logger.error(f"API Error: {error}")
    return {
        'success': False,
        'error': 'api_error',
        'message': 'API service unavailable. Please try again.',
        'recoverable': True
    }

def handle_clip_error(error: Exception) -> Dict[str, Any]:
    """Handle clip fetching errors"""
    logger.error(f"Clip Error: {error}")
    return {
        'success': False,
        'error': 'clip_error',
        'message': 'Unable to fetch video clips. Try different prompt.',
        'recoverable': True
    }

def handle_edit_error(error: Exception) -> Dict[str, Any]:
    """Handle video editing errors"""
    logger.error(f"Edit Error: {error}")
    return {
        'success': False,
        'error': 'edit_error',
        'message': 'Video editing failed. Please try again.',
        'recoverable': True
    }

def handle_timeout_error(error: Exception) -> Dict[str, Any]:
    """Handle timeout errors"""
    logger.error(f"Timeout Error: {error}")
    return {
        'success': False,
        'error': 'timeout',
        'message': 'Generation timeout. Switching to fallback mode.',
        'recoverable': True
    }

def handle_unknown_error(error: Exception) -> Dict[str, Any]:
    """Handle unknown errors"""
    logger.error(f"Unknown Error: {error}")
    return {
        'success': False,
        'error': 'unknown',
        'message': 'An unexpected error occurred.',
        'recoverable': False
    }

def get_user_friendly_message(error_type: str) -> str:
    """Get user-friendly error message"""
    messages = {
        'api_error': 'Service temporarily unavailable. Retrying...',
        'clip_error': 'No matching clips found. Try different keywords.',
        'edit_error': 'Video processing failed. Please try again.',
        'timeout': 'Request taking too long. Using fallback mode.',
        'unknown': 'Something went wrong. Please try again.'
    }
    return messages.get(error_type, messages['unknown'])
