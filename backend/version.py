"""
Version Information
"""

__version__ = "2.0.0"
__author__ = "NEXUS VISION Team"
__license__ = "MIT"

VERSION_INFO = {
    'major': 2,
    'minor': 0,
    'patch': 0,
    'release': 'stable'
}

FEATURES = [
    'Video Generation',
    'Video Effects',
    'Color Grading',
    'Subtitles',
    'Watermarks',
    'Stabilization',
    'Audio Effects',
    'Batch Processing',
    'Export Manager',
    'Analytics'
]

def get_version():
    return __version__

def get_features():
    return FEATURES
