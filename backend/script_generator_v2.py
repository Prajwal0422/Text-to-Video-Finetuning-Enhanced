"""
NEXUS VISION - Smart Scene Generator V2
Generates contextual scenes that match prompt semantics
"""

import re
import spacy
from typing import List, Dict, Set

class SmartScriptGenerator:
    def __init__(self):
        # Try to load spacy model, fallback to simple extraction
        try:
            self.nlp = spacy.load("en_core_web_sm")
            self.use_nlp = True
        except:
            self.use_nlp = False
            print("⚠️  spaCy not available, using simple extraction")
        
        # Context words for different categories
        self.context_words = {
            'traffic': ['highway', 'road', 'cars', 'vehicles', 'busy', 'congestion'],
            'nature': ['landscape', 'scenic', 'natural', 'outdoor', 'environment'],
            'city': ['urban', 'downtown', 'street', 'buildings', 'metropolitan'],
            'water': ['ocean', 'sea', 'waves', 'beach', 'coast', 'shore'],
            'sky': ['clouds', 'sunset', 'sunrise', 'aerial', 'atmosphere'],
            'people': ['crowd', 'person', 'human', 'walking', 'activity'],
            'motion': ['moving', 'fast', 'slow', 'flowing', 'dynamic']
        }
    
    def extract_nouns_and_verbs(self, prompt: str) -> Dict[str, List[str]]:
        """Extract nouns and verbs using NLP or simple patterns"""
        if self.use_nlp:
            doc = self.nlp(prompt.lower())
            nouns = [token.text for token in doc if token.pos_ == "NOUN"]
            verbs = [token.text for token in doc if token.pos_ == "VERB"]
            adjectives = [token.text for token in doc if token.pos_ == "ADJ"]
        else:
            # Simple extraction
            words = re.findall(r'\b[a-z]+\b', prompt.lower())
            # Common nouns and verbs (simplified)
            motion_verbs = {'moving', 'driving', 'walking', 'running', 'flying', 'flowing', 'falling'}
            nouns = [w for w in words if len(w) > 3 and w not in motion_verbs]
            verbs = [w for w in words if w in motion_verbs]
            adjectives = []
        
        return {
            'nouns': nouns[:5],
            'verbs': verbs[:3],
            'adjectives': adjectives[:3]
        }
    
    def add_context_words(self, base_words: List[str]) -> List[str]:
        """Add relevant context words based on base words"""
        context = set()
        
        for word in base_words:
            for category, related_words in self.context_words.items():
                if word in related_words or category in word:
                    context.update(related_words[:2])
        
        return list(context)[:3]
    
    def generate_scene_queries(self, prompt: str) -> List[Dict[str, any]]:
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
            'query': ' '.join(scene1_words[:4]),  # Max 4 words
            'keywords': scene1_words[:4],
            'duration': 3.0,
            'description': f"Primary scene: {' '.join(scene1_words[:3])}"
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
            'description': f"Context scene: {' '.join(scene2_words[:3])}"
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
            'description': f"Action scene: {' '.join(scene3_words[:3])}"
        })
        
        return scenes
    
    def generate_script(self, prompt: str) -> Dict:
        """Generate complete script with smart scenes"""
        scenes = self.generate_scene_queries(prompt)
        
        # Extract all unique keywords
        all_keywords = set()
        for scene in scenes:
            all_keywords.update(scene['keywords'])
        
        return {
            'prompt': prompt,
            'keywords': list(all_keywords),
            'scenes': scenes,
            'total_duration': sum(s['duration'] for s in scenes),
            'scene_count': len(scenes)
        }


# Backward compatibility
class ScriptGenerator(SmartScriptGenerator):
    """Alias for backward compatibility"""
    pass


if __name__ == "__main__":
    # Test with example prompts
    generator = SmartScriptGenerator()
    
    test_prompts = [
        "A car moving in heavy traffic",
        "Sunset over beach with waves",
        "City night time lapse with lights"
    ]
    
    for prompt in test_prompts:
        print(f"\n{'='*60}")
        print(f"Prompt: {prompt}")
        print('='*60)
        
        script = generator.generate_script(prompt)
        
        print(f"Keywords: {script['keywords']}")
        print(f"Scenes ({script['scene_count']}):")
        for scene in script['scenes']:
            print(f"  Scene {scene['id']}: {scene['query']}")
            print(f"    Keywords: {scene['keywords']}")
            print(f"    Duration: {scene['duration']}s")
