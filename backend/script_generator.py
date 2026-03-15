"""
NEXUS VISION - Smart Scene Generator
Generates contextual scenes that match prompt semantics
"""

import re
from typing import List, Dict, Set

class ScriptGenerator:
    def __init__(self):
        # Context words for different categories
        self.context_words = {
            'traffic': ['highway', 'road', 'cars', 'vehicles', 'busy', 'congestion', 'jam'],
            'nature': ['landscape', 'scenic', 'natural', 'outdoor', 'environment', 'wild'],
            'city': ['urban', 'downtown', 'street', 'buildings', 'metropolitan', 'skyline'],
            'water': ['ocean', 'sea', 'waves', 'beach', 'coast', 'shore', 'lake'],
            'sky': ['clouds', 'sunset', 'sunrise', 'aerial', 'atmosphere', 'horizon'],
            'people': ['crowd', 'person', 'human', 'walking', 'activity', 'group'],
            'motion': ['moving', 'fast', 'slow', 'flowing', 'dynamic', 'speed']
        }
        
        # Motion verbs
        self.motion_verbs = {
            'moving', 'driving', 'walking', 'running', 'flying', 'flowing', 
            'falling', 'rising', 'traveling', 'cruising', 'racing'
        }
    
    def extract_nouns_and_verbs(self, prompt: str) -> Dict[str, List[str]]:
        """Extract nouns and verbs from prompt with improved detection"""
        words = re.findall(r'\b[a-z]+\b', prompt.lower())
        
        # Stop words to remove
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                     'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be', 'been'}
        
        # Expanded motion verbs
        motion_verbs = {
            'moving', 'driving', 'walking', 'running', 'flying', 'flowing', 
            'falling', 'rising', 'traveling', 'cruising', 'racing', 'swimming',
            'jumping', 'dancing', 'fighting', 'struggling', 'working', 'playing'
        }
        
        # Extract verbs (motion words)
        verbs = [w for w in words if w in motion_verbs]
        
        # Extract nouns (content words not in stop words)
        nouns = [w for w in words if w not in stop_words and w not in motion_verbs and len(w) > 2]
        
        return {
            'nouns': nouns[:6],  # Get more nouns
            'verbs': verbs[:3]
        }
    
    def add_context_words(self, base_words: List[str]) -> List[str]:
        """Add relevant context words based on base words"""
        context = set()
        
        for word in base_words:
            for category, related_words in self.context_words.items():
                if word in related_words or category in word or word in category:
                    context.update(related_words[:2])
        
        return list(context)[:3]
    
    def generate_scenes(self, prompt: str) -> List[Dict[str, any]]:
        """Generate 3 structured scene queries"""
        # Extract linguistic components
        components = self.extract_nouns_and_verbs(prompt)
        nouns = components['nouns']
        verbs = components['verbs']
        
        if not nouns:
            nouns = ['nature', 'landscape']
        
        scenes = []
        
        # Scene 1: Primary subject with main action
        scene1_words = []
        if nouns:
            scene1_words.append(nouns[0])
        if verbs:
            scene1_words.append(verbs[0])
        if len(nouns) > 1:
            scene1_words.append(nouns[1])
        
        # Add context
        context1 = self.add_context_words(scene1_words)
        scene1_words.extend(context1[:1])
        
        scenes.append({
            'id': 1,
            'query': ' '.join(scene1_words[:4]),
            'keywords': scene1_words[:4],
            'duration': 3.0,
            'description': f"Primary: {' '.join(scene1_words[:3])}"
        })
        
        # Scene 2: Secondary perspective with context
        scene2_words = []
        if len(nouns) > 1:
            scene2_words.append(nouns[1])
        elif nouns:
            scene2_words.append(nouns[0])
        
        # Add different context
        context2 = self.add_context_words(nouns)
        scene2_words.extend([w for w in context2 if w not in scene2_words][:2])
        
        if nouns and nouns[0] not in scene2_words:
            scene2_words.append(nouns[0])
        
        scenes.append({
            'id': 2,
            'query': ' '.join(scene2_words[:4]),
            'keywords': scene2_words[:4],
            'duration': 3.0,
            'description': f"Context: {' '.join(scene2_words[:3])}"
        })
        
        # Scene 3: Variation with action
        scene3_words = []
        if verbs:
            scene3_words.append(verbs[0])
        if nouns:
            scene3_words.append(nouns[0])
        
        # Add more context
        remaining_nouns = [n for n in nouns if n not in scene3_words]
        scene3_words.extend(remaining_nouns[:2])
        
        scenes.append({
            'id': 3,
            'query': ' '.join(scene3_words[:4]),
            'keywords': scene3_words[:4],
            'duration': 3.0,
            'description': f"Action: {' '.join(scene3_words[:3])}"
        })
        
        return scenes
    
    def generate_script(self, prompt: str) -> Dict:
        """Main method to generate complete script"""
        scenes = self.generate_scenes(prompt)
        
        # Extract all unique keywords
        all_keywords = set()
        for scene in scenes:
            all_keywords.update(scene['keywords'])
        
        return {
            'prompt': prompt,
            'keywords': list(all_keywords),
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
