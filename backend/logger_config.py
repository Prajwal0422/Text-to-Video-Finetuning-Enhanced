"""
Logging Configuration
Centralized logging setup for the application
"""

import logging
import sys
from datetime import datetime

def setup_logger(name: str, level=logging.INFO):
    """
    Setup logger with consistent formatting
    
    Args:
        name: Logger name
        level: Logging level
    
    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove existing handlers
    logger.handlers = []
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    
    return logger

def log_generation_start(prompt: str):
    """Log generation start"""
    logger = logging.getLogger('video_generation')
    logger.info(f"Starting generation: '{prompt}'")

def log_generation_complete(prompt: str, duration: float):
    """Log generation completion"""
    logger = logging.getLogger('video_generation')
    logger.info(f"Completed: '{prompt}' in {duration:.1f}s")

def log_generation_error(prompt: str, error: str):
    """Log generation error"""
    logger = logging.getLogger('video_generation')
    logger.error(f"Failed: '{prompt}' - {error}")
