"""
NEXUS VISION - AI Scene Planner
Converts prompts into detailed, contextual scenes for video generation
"""

import re
from typing import List, Dict, Tuple

class AIScenePlanner:
    def __init__(self):
        # Scene context database
        self.scene_contexts = {
            'traffic': {
                'subjects': ['cars', 'vehicles', 'automobiles', 'trucks'],
                'actions': ['moving', 'driving', 'traveling', 'cruising'],
                'settings': ['highway', 'road', 'street', 'freeway', 'intersection'],
                'modifiers': ['busy', 'heavy', 'congested', 'rush hour', 'slow']
            },
            'nature': {
                'subjects': ['trees', 'mountains', 'forest', 'wildlife', 'plants'],
                'actions': ['flowing', 'swaying', 'growing', 'blooming'],
                'settings': ['landscape', 'wilderness', 'park', 'valley', 'meadow'],
                'modifiers': ['beautiful', 'serene', 'peaceful', 'natural', 'scenic']
            },
            'water': {
                'subjects': ['waves', 'ocean', 'sea', 'lake', 'river'],
                'actions': ['crashing', 'flowing', 'rippling', 'splashing'],
                'settings': ['beach', 'coast', 'shore', 'waterfront', 'bay'],
                'modifiers': ['calm', 'turbulent', 'crystal', 'blue', 'clear']
            },
            'city': {
                'subjects': ['buildings', 'skyscrapers', 'streets', 'people', 'lights'],
                'actions': ['bustling', 'moving', 'walking', 'working'],
                'settings': ['downtown', 'urban', 'metropolitan', 'cityscape', 'plaza'],
                'modifiers': ['modern', 'busy', 'vibrant', 'crowded', 'illuminated']
            },
            'sky': {
                'subjects': ['clouds', 'sun', 'moon', 'stars', 'birds'],
                'actions': ['floating', 'drifting', 'flying', 'soaring'],
                'settings': ['horizon', 'atmosphere', 'skyline', 'aerial'],
                'modifiers': ['beautiful', 'dramatic', 'colorful', 'golden', 'bright']
            }
        }
        
        # Motion verbs
        self.motion_verbs = {
            'moving', 'driving', 'walking', 'running', 'flying', 'flowing',
            'falling', 'rising', 'traveling', 'cruising', 'racing', 'drifting',
            'floating', 'soaring', 'crashing', 'splashing', 'swaying'
        }
        
        # Time/lighting keywords
        self.time_keywords = {
            'sunset', 'sunrise', 'dawn', 'dusk', 'night', 'day',
            'morning', 'evening', 'afternoon', 'golden hour'
        }
    
    def extract_components(self, prompt: str) -> Dict[str, List[str]]:
        """Extract subjects, actions, settings, and modifiers from prompt"""
        words = re.findall(r'\b[a-z]+\b', prompt.lower())
        
        # Stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
            'for', 'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are'
        }
        
        # Filter words
        content_words = [w for w in words if w not in stop_words and len(w) > 2]
        
        # Categorize
        subjects = []
        actions = []
        settings = []
        modifiers = []
        time_context = []
        
        for word in content_words:
            if word in self.motion_verbs:
                actions.append(word)
            elif word in self.time_keywords:
                time_context.append(word)
            else:
                # Check against context database
                found = False
                for category, context in self.scene_contexts.items():
                    if word in context['subjects']:
                        subjects.append(word)
                        found = True
                    elif word in context['settings']:
                        settings.append(word)
                        found = True
                    elif word in context['modifiers']:
                        modifiers.append(word)
                        found = True
                
                if not found and len(word) > 3:
                    subjects.append(word)  # Default to subject
        
        return {
            'subjects': subjects[:3],
            'actions': actions[:2],
            'settings': settings[:2],
            'modifiers': modifiers[:2],
            'time': time_context[:1]
        }
    
    def detect_category(self, components: Dict[str, List[str]]) -> str:
        """Detect the main category of the scene"""
        all_words = (
            components['subjects'] + 
            components['settings'] + 
            components['modifiers']
        )
        
        # Score each category
        category_scores = {}
        for category, context in self.scene_contexts.items():
            score = 0
            all_context_words = (
                context['subjects'] + 
                context['settings'] + 
                context['modifiers']
            )
            for word in all_words:
                if word in all_context_words:
                    score += 1
            category_scores[category] = score
        
        # Return highest scoring category
        if category_scores:
            return max(category_scores, key=category_scores.get)
        return 'nature'  # Default
    
    def generate_scene_variations(self, components: Dict[str, List[str]], 
                                  category: str) -> List[Dict[str, any]]:
        """Generate 3 detailed scene variations"""
        context = self.scene_contexts.get(category, self.scene_contexts['nature'])
        
        subjects = components['subjects'] or context['subjects'][:1]
        actions = components['actions'] or context['actions'][:1]
        settings = components['settings'] or context['settings'][:1]
        modifiers = components['modifiers'] or context['modifiers'][:1]
        time_ctx = components['time']
        
        scenes = []
        
        # Scene 1: Primary - Main subject with action
        scene1_words = []
        if subjects:
            scene1_words.append(subjects[0])
        if actions:
            scene1_words.append(actions[0])
        if settings:
            scene1_words.append(settings[0])
        if modifiers:
            scene1_words.append(modifiers[0])
        
        scenes.append({
            'id': 1,
            'type': 'primary',
            'query': ' '.join(scene1_words[:4]),
            'keywords': scene1_words[:4],
            'description': f"Main scene: {' '.join(scene1_words[:3])}",
            'duration': 3.0,
            'category': category
        })
        
        # Scene 2: Context - Setting with modifiers
        scene2_words = []
        if settings:
            scene2_words.append(settings[0])
        if len(subjects) > 1:
            scene2_words.append(subjects[1])
        elif subjects:
            scene2_words.append(subjects[0])
        
        # Add context from category
        scene2_words.extend([w for w in context['settings'][:1] if w not in scene2_words])
        scene2_words.extend([w for w in context['subjects'][:1] if w not in scene2_words])
        
        scenes.append({
            'id': 2,
            'type': 'context',
            'query': ' '.join(scene2_words[:4]),
            'keywords': scene2_words[:4],
            'description': f"Context scene: {' '.join(scene2_words[:3])}",
            'duration': 3.0,
            'category': category
        })
        
        # Scene 3: Detail - Action with time context
        scene3_words = []
        if time_ctx:
            scene3_words.append(time_ctx[0])
        if actions:
            scene3_words.append(actions[0])
        if subjects:
            scene3_words.append(subjects[0])
        
        # Add variety
        scene3_words.extend([w for w in context['modifiers'][:1] if w not in scene3_words])
        
        scenes.append({
            'id': 3,
            'type': 'detail',
            'query': ' '.join(scene3_words[:4]),
            'keywords': scene3_words[:4],
            'description': f"Detail scene: {' '.join(scene3_words[:3])}",
            'duration': 3.0,
            'category': category
        })
        
        return scenes
    
    def plan_scenes(self, prompt: str) -> Dict[str, any]:
        """Main method: Convert prompt into detailed scene plan"""
        # Extract components
        components = self.extract_components(prompt)
        
        # Detect category
        category = self.detect_category(components)
        
        # Generate scenes
        scenes = self.generate_scene_variations(components, category)
        
        return {
            'prompt': prompt,
            'category': category,
            'components': components,
            'scenes': scenes,
            'total_duration': sum(s['duration'] for s in scenes),
            'scene_count': len(scenes)
        }


if __name__ == "__main__":
    # Test the AI Scene Planner
    planner = AIScenePlanner()
    
    test_prompts = [
        "A car moving in heavy traffic",
        "Sunset over beach with waves",
        "City night time lapse with lights",
        "Forest with trees swaying in wind"
    ]
    
    for prompt in test_prompts:
        print(f"\n{'='*70}")
        print(f"Prompt: {prompt}")
        print('='*70)
        
        plan = planner.plan_scenes(prompt)
        
        print(f"Category: {plan['category']}")
        print(f"Components: {plan['components']}")
        print(f"\nScenes ({plan['scene_count']}):")
        for scene in plan['scenes']:
            print(f"  Scene {scene['id']} ({scene['type']}): {scene['query']}")
            print(f"    Description: {scene['description']}")
            print(f"    Duration: {scene['duration']}s")
