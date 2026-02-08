"""
Script Generator - Converts text prompts into scene descriptions
Uses simple keyword extraction and scene breakdown
"""

import re
from typing import List, Dict

class ScriptGenerator:
    def __init__(self):
        self.scene_templates = [
            "establishing shot of {subject}",
            "close-up of {subject}",
            "wide angle view of {subject}",
            "{subject} in motion",
            "detailed view of {subject}"
        ]
    
    def extract_keywords(self, prompt: str) -> List[str]:
        """Extract visual keywords from prompt"""
        # Remove common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                     'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
                     'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
                     'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that'}
        
        # Clean and split
        words = re.findall(r'\b[a-z]+\b', prompt.lower())
        keywords = [w for w in words if w not in stop_words and len(w) > 3]
        
        # Return top keywords (max 5)
        return keywords[:5] if keywords else ['nature', 'landscape']
    
    def generate_scenes(self, prompt: str) -> List[Dict[str, str]]:
        """Generate 3-5 scene descriptions from prompt"""
        keywords = self.extract_keywords(prompt)
        
        scenes = []
        
        # Generate scenes based on keywords
        for i, keyword in enumerate(keywords[:5]):
            scene = {
                'id': i + 1,
                'description': f"Scene showing {keyword}",
                'keywords': [keyword],
                'duration': 3.0  # seconds per clip
            }
            scenes.append(scene)
        
        # Ensure at least 3 scenes
        while len(scenes) < 3:
            scenes.append({
                'id': len(scenes) + 1,
                'description': f"Scene showing {keywords[0] if keywords else 'nature'}",
                'keywords': keywords[:1] if keywords else ['nature'],
                'duration': 3.0
            })
        
        return scenes
    
    def generate_script(self, prompt: str) -> Dict:
        """Main method to generate complete script"""
        keywords = self.extract_keywords(prompt)
        scenes = self.generate_scenes(prompt)
        
        return {
            'prompt': prompt,
            'keywords': keywords,
            'scenes': scenes,
            'total_duration': sum(s['duration'] for s in scenes)
        }


if __name__ == "__main__":
    # Test
    generator = ScriptGenerator()
    script = generator.generate_script("A beautiful sunset over mountains with birds flying")
    print("Generated Script:")
    print(f"Keywords: {script['keywords']}")
    print(f"Scenes: {len(script['scenes'])}")
    for scene in script['scenes']:
        print(f"  - {scene['description']}")
