"""
Template Manager
Manages video templates and presets
"""

from typing import Dict, List, Optional
import json
import os

class VideoTemplate:
    """Video template with predefined settings"""
    
    def __init__(
        self,
        name: str,
        description: str,
        duration: float,
        resolution: tuple,
        fps: int,
        style: str,
        scenes: List[Dict]
    ):
        self.name = name
        self.description = description
        self.duration = duration
        self.resolution = resolution
        self.fps = fps
        self.style = style
        self.scenes = scenes
    
    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'description': self.description,
            'duration': self.duration,
            'resolution': self.resolution,
            'fps': self.fps,
            'style': self.style,
            'scenes': self.scenes
        }


class TemplateManager:
    """Manages video templates"""
    
    def __init__(self, templates_dir: str = "templates"):
        self.templates_dir = templates_dir
        os.makedirs(templates_dir, exist_ok=True)
        self.templates: Dict[str, VideoTemplate] = {}
        self._load_default_templates()
    
    def _load_default_templates(self):
        """Load default templates"""
        
        # Social Media Template
        self.add_template(VideoTemplate(
            name='social_media',
            description='Optimized for social media platforms',
            duration=15.0,
            resolution=(1080, 1080),
            fps=30,
            style='dynamic',
            scenes=[
                {'type': 'intro', 'duration': 3},
                {'type': 'main', 'duration': 9},
                {'type': 'outro', 'duration': 3}
            ]
        ))
        
        # YouTube Template
        self.add_template(VideoTemplate(
            name='youtube',
            description='Standard YouTube video format',
            duration=60.0,
            resolution=(1920, 1080),
            fps=30,
            style='cinematic',
            scenes=[
                {'type': 'intro', 'duration': 5},
                {'type': 'main', 'duration': 50},
                {'type': 'outro', 'duration': 5}
            ]
        ))
        
        # TikTok Template
        self.add_template(VideoTemplate(
            name='tiktok',
            description='Vertical format for TikTok',
            duration=30.0,
            resolution=(1080, 1920),
            fps=30,
            style='energetic',
            scenes=[
                {'type': 'hook', 'duration': 3},
                {'type': 'content', 'duration': 24},
                {'type': 'cta', 'duration': 3}
            ]
        ))
        
        # Story Template
        self.add_template(VideoTemplate(
            name='story',
            description='Instagram/Facebook story format',
            duration=15.0,
            resolution=(1080, 1920),
            fps=30,
            style='casual',
            scenes=[
                {'type': 'main', 'duration': 15}
            ]
        ))
    
    def add_template(self, template: VideoTemplate):
        """Add a template"""
        self.templates[template.name] = template
    
    def get_template(self, name: str) -> Optional[VideoTemplate]:
        """Get template by name"""
        return self.templates.get(name)
    
    def list_templates(self) -> List[Dict]:
        """List all templates"""
        return [t.to_dict() for t in self.templates.values()]
    
    def save_template(self, template: VideoTemplate):
        """Save template to file"""
        filepath = os.path.join(self.templates_dir, f"{template.name}.json")
        
        with open(filepath, 'w') as f:
            json.dump(template.to_dict(), f, indent=2)
    
    def load_template(self, name: str) -> Optional[VideoTemplate]:
        """Load template from file"""
        filepath = os.path.join(self.templates_dir, f"{name}.json")
        
        if not os.path.exists(filepath):
            return None
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        return VideoTemplate(**data)
    
    def apply_template(
        self,
        template_name: str,
        prompt: str
    ) -> Dict:
        """Apply template to generation"""
        template = self.get_template(template_name)
        
        if not template:
            raise ValueError(f"Template not found: {template_name}")
        
        return {
            'prompt': prompt,
            'template': template.to_dict(),
            'settings': {
                'duration': template.duration,
                'resolution': template.resolution,
                'fps': template.fps,
                'style': template.style
            }
        }


if __name__ == "__main__":
    manager = TemplateManager()
    
    print("Available Templates:")
    for template in manager.list_templates():
        print(f"  - {template['name']}: {template['description']}")
