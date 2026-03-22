"""
Application Constants
Centralized configuration values
"""

# Video Settings
DEFAULT_FPS = 24
DEFAULT_RESOLUTION = (1920, 1080)
DEFAULT_DURATION = 12
MIN_CLIP_DURATION = 4
MAX_CLIP_DURATION = 16

# Generation Settings
MAX_RETRIES = 3
RETRY_DELAYS = [5, 10, 20]  # seconds
TIMEOUT_SECONDS = 60
MAX_CLIPS_PER_VIDEO = 5

# API Settings
PEXELS_API_URL = "https://api.pexels.com/videos/search"
API_TIMEOUT = 30
MAX_API_RESULTS = 15

# Cache Settings
CACHE_DIR = "outputs/cache"
NORMALIZED_DIR = "outputs/normalized"
VIDEO_OUTPUT_DIR = "outputs/videos"
MAX_CACHE_SIZE_MB = 500

# File Settings
ALLOWED_VIDEO_FORMATS = ['.mp4', '.avi', '.mov', '.webm']
OUTPUT_FORMAT = 'mp4'
OUTPUT_CODEC = 'libx264'

# Performance Settings
THREAD_POOL_SIZE = 4
PARALLEL_DOWNLOADS = 3

# UI Settings
WEBSOCKET_PING_INTERVAL = 30
PROGRESS_UPDATE_INTERVAL = 0.5

# Error Messages
ERROR_NO_CLIPS = "No video clips found for this prompt"
ERROR_API_LIMIT = "API rate limit reached"
ERROR_TIMEOUT = "Generation timeout"
ERROR_NETWORK = "Network connection error"

# Success Messages
SUCCESS_GENERATION = "Video created successfully"
SUCCESS_DOWNLOAD = "Clip downloaded"
SUCCESS_EXPORT = "Video exported"
