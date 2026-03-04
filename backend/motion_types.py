"""
Motion Types Configuration
Defines all available motion types and their parameters
"""

MOTION_TYPES = {
    "zoom_in": {
        "name": "Zoom In",
        "description": "Smooth zoom into the image",
        "intensity": 0.5,
        "best_for": ["portraits", "details", "close-ups"]
    },
    "zoom_out": {
        "name": "Zoom Out",
        "description": "Smooth zoom out from the image",
        "intensity": 0.5,
        "best_for": ["reveals", "landscapes", "wide shots"]
    },
    "pan_right": {
        "name": "Pan Right",
        "description": "Pan from left to right",
        "intensity": 0.7,
        "best_for": ["landscapes", "cityscapes", "horizons"]
    },
    "pan_left": {
        "name": "Pan Left",
        "description": "Pan from right to left",
        "intensity": 0.7,
        "best_for": ["landscapes", "cityscapes", "horizons"]
    },
    "pan_up": {
        "name": "Pan Up",
        "description": "Pan from bottom to top",
        "intensity": 0.7,
        "best_for": ["tall subjects", "buildings", "trees"]
    },
    "pan_down": {
        "name": "Pan Down",
        "description": "Pan from top to bottom",
        "intensity": 0.7,
        "best_for": ["aerial views", "waterfalls", "descents"]
    },
    "rotate_cw": {
        "name": "Rotate Clockwise",
        "description": "Clockwise rotation",
        "intensity": 0.8,
        "best_for": ["dynamic scenes", "action", "energy"]
    },
    "rotate_ccw": {
        "name": "Rotate Counter-Clockwise",
        "description": "Counter-clockwise rotation",
        "intensity": 0.8,
        "best_for": ["dynamic scenes", "action", "energy"]
    },
    "ken_burns": {
        "name": "Ken Burns",
        "description": "Pan and zoom combination",
        "intensity": 0.6,
        "best_for": ["documentaries", "storytelling", "photos"]
    },
    "dolly_zoom": {
        "name": "Dolly Zoom",
        "description": "Vertigo effect (zoom + dolly)",
        "intensity": 0.9,
        "best_for": ["dramatic moments", "reveals", "tension"]
    },
    "breathe": {
        "name": "Breathe",
        "description": "Subtle breathing motion",
        "intensity": 0.3,
        "best_for": ["calm scenes", "meditation", "peaceful"]
    }
}


def get_motion_type_info(motion_type: str) -> dict:
    """Get information about a motion type"""
    return MOTION_TYPES.get(motion_type, MOTION_TYPES["zoom_in"])


def list_motion_types() -> list:
    """List all available motion types"""
    return list(MOTION_TYPES.keys())


def get_recommended_motion(keywords: list) -> str:
    """Recommend motion type based on keywords"""
    keyword_str = " ".join(keywords).lower()
    
    for motion_type, info in MOTION_TYPES.items():
        for best_for in info["best_for"]:
            if best_for in keyword_str:
                return motion_type
    
    return "zoom_in"  # Default
