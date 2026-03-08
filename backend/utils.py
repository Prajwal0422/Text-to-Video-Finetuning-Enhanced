"""
NEXUS VISION - Utility Functions
Common utility functions used across the application
"""

import os
import hashlib
from pathlib import Path
from typing import Optional, Union
from datetime import datetime

def get_file_size(file_path: Union[str, Path]) -> str:
    """
    Get human-readable file size
    
    Args:
        file_path: Path to file
    
    Returns:
        Formatted file size string (e.g., "2.5 MB")
    """
    size_bytes = os.path.getsize(file_path)
    
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    
    return f"{size_bytes:.1f} TB"

def generate_hash(text: str) -> str:
    """
    Generate MD5 hash of text
    
    Args:
        text: Input text
    
    Returns:
        MD5 hash string
    """
    return hashlib.md5(text.encode()).hexdigest()

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing invalid characters
    
    Args:
        filename: Original filename
    
    Returns:
        Sanitized filename
    """
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def get_timestamp() -> str:
    """
    Get current timestamp string
    
    Returns:
        Formatted timestamp (YYYYMMDD_HHMMSS)
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def format_duration(seconds: float) -> str:
    """
    Format duration in seconds to human-readable string
    
    Args:
        seconds: Duration in seconds
    
    Returns:
        Formatted duration string (e.g., "1m 30s")
    """
    if seconds < 60:
        return f"{seconds:.1f}s"
    
    minutes = int(seconds // 60)
    remaining_seconds = seconds % 60
    
    if minutes < 60:
        return f"{minutes}m {remaining_seconds:.0f}s"
    
    hours = int(minutes // 60)
    remaining_minutes = minutes % 60
    return f"{hours}h {remaining_minutes}m"

def ensure_dir(directory: Union[str, Path]) -> Path:
    """
    Ensure directory exists, create if it doesn't
    
    Args:
        directory: Directory path
    
    Returns:
        Path object
    """
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    return path

def clean_old_files(directory: Union[str, Path], max_age_days: int = 7):
    """
    Clean files older than specified days
    
    Args:
        directory: Directory to clean
        max_age_days: Maximum age in days
    """
    path = Path(directory)
    if not path.exists():
        return
    
    current_time = datetime.now().timestamp()
    max_age_seconds = max_age_days * 24 * 60 * 60
    
    for file in path.iterdir():
        if file.is_file():
            file_age = current_time - file.stat().st_mtime
            if file_age > max_age_seconds:
                file.unlink()

def get_cache_size(directory: Union[str, Path]) -> int:
    """
    Get total size of directory in bytes
    
    Args:
        directory: Directory path
    
    Returns:
        Total size in bytes
    """
    path = Path(directory)
    if not path.exists():
        return 0
    
    total_size = 0
    for file in path.rglob('*'):
        if file.is_file():
            total_size += file.stat().st_size
    
    return total_size
