"""
NEXUS VISION - Cinematic Prompt Engine
Converts raw prompts into structured cinematic scenes with visual nouns
Removes abstract concepts and converts emotions into visual metaphors
"""

import re
from typing import List, Dict, Tuple

class CinematicPromptEngine:
    def __init__(self):
        # Visual noun database - concrete, filmable objects
        self.visual_nouns = {
            # Military & War
            'military': ['tanks', 'soldiers', 'battlefield', 'smoke', 'explosion', 'weapons'],
            'war': ['combat', 'battlefield', 'smoke', 'ruins', 'destroyed buildings', 'fire'],
            'tanks': ['armored vehicles', 'military tanks', 'battlefield', 'dust', 'convoy'],
            'soldiers': ['troops', 'military personnel', 'combat gear', 'uniforms', 'weapons'],
            'army': ['military forces', 'troops', 'vehicles', 'equipment', 'base'],
            'combat': ['fighting', 'action', 'smoke', 'explosions', 'chaos'],
            'battle': ['warfare', 'conflict zone', 'smoke', 'fire', 'destruction'],
            'fighter': ['jets', 'aircraft', 'sky', 'clouds', 'flying'],
            'airforce': ['jets', 'aircraft', 'helicopters', 'sky', 'flying'],
            
            # Nature & Environment
            'sunset': ['golden sky', 'horizon', 'clouds', 'orange light', 'silhouettes'],
            'ocean': ['waves', 'water', 'coast', 'beach', 'horizon'],
            'mountains': ['peaks', 'landscape', 'rocks', 'valleys', 'summit'],
            'forest': ['trees', 'woodland', 'vegetation', 'path', 'nature'],
            'rain': ['rainfall', 'water drops', 'wet surfaces', 'clouds', 'storm'],
            
            # Urban & City
            'city': ['buildings', 'streets', 'skyline', 'lights', 'traffic'],
            'traffic': ['cars', 'vehicles', 'highway', 'road', 'movement'],
            'street': ['urban road', 'buildings', 'sidewalk', 'vehicles', 'lights'],
            
            # Abstract to Visual Conversion
            'struggle': ['difficult terrain', 'harsh conditions', 'smoke', 'chaos'],
            'dying': ['fallen', 'ruins', 'destruction', 'smoke', 'aftermath'],
            'fighting': ['combat action', 'smoke', 'movement', 'chaos', 'intensity'],
            'conflict': ['confrontation', 'smoke', 'destruction', 'chaos', 'ruins'],
            'destruction': ['ruins', 'debris', 'smoke', 'fire', 'damaged buildings'],
            'chaos': ['smoke', 'movement', 'disorder', 'intensity', 'action']
        }
        
        # Cinematic scene templates
        self.scene_templates = {
            'military': [
                'military tanks battlefield smoke explosion',
                'soldiers combat gear war zone action',
                'armored vehicles convoy dust movement',
                'military base equipment troops training'
            ],
            'war': [
                'battlefield smoke fire destruction ruins',
                'combat zone soldiers action chaos',
                'destroyed buildings debris smoke aftermath',
                'war zone military vehicles movement'
            ],
            'airforce': [
                'fighter jets flying sky clouds combat',
                'military aircraft formation aerial view',
                'helicopters flying war zone smoke',
                'jets sky clouds speed motion'
            ],
            'nature': [
                'landscape scenic mountains sky clouds',
                'ocean waves water coast horizon',
                'forest trees woodland nature green',
                'sunset golden sky clouds horizon'
            ],
            'urban': [
                'city skyline buildings lights night',
                'traffic cars highway road movement',
                'urban street buildings vehicles lights',
                'downtown buildings architecture skyline'
            ]
        }
        
        # Emotion to visual metaphor mapping
        self.emotion_to_visual = {
            'struggle': 'harsh terrain smoke difficulty',
            'dying': 'fallen ruins aftermath smoke',
            'pain': 'destruction chaos smoke fire',
            'fear': 'dark shadows smoke chaos',
            'anger': 'fire smoke intensity chaos',
            'sadness': 'ruins aftermath destruction grey',
            'hope': 'light rays sky horizon',
            'victory': 'clear sky triumph aftermath'
        }
    
    def extract_key_subjects(self, prompt: str) -> List[str]:
        """Extract main subjects from prompt"""
        prompt_lower = prompt.lower()
        
        # Remove common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                     'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be'}
        
        words = re.findall(r'\b[a-z]+\b', prompt_lower)
        subjects = [w for w in words if w not in stop_words and len(w) > 3]
        
        return subjects[:8]  # Top 8 subjects
    
    def convert_abstract_to_visual(self, word: str) -> List[str]:
        """Convert abstract concepts to visual elements"""
        if word in self.emotion_to_visual:
            return self.emotion_to_visual[word].split()
        
        if word in self.visual_nouns:
            return self.visual_nouns[word][:3]
        
        return [word]
    
    def detect_primary_category(self, subjects: List[str]) -> str:
        """Detect primary category from subjects"""
        category_scores = {
            'military': 0,
            'war': 0,
            'airforce': 0,
            'nature': 0,
            'urban': 0
        }
        
        military_keywords = {'military', 'tank', 'soldier', 'army', 'combat', 'weapon', 'troops'}
        war_keywords = {'war', 'battle', 'fight', 'conflict', 'destruction', 'battlefield'}
        airforce_keywords = {'jet', 'aircraft', 'helicopter', 'flying', 'airforce', 'fighter'}
        nature_keywords = {'sunset', 'ocean', 'mountain', 'forest', 'nature', 'landscape'}
        urban_keywords = {'city', 'traffic', 'street', 'urban', 'building', 'downtown'}
        
        for subject in subjects:
            if subject in military_keywords:
                category_scores['military'] += 2
            if subject in war_keywords:
                category_scores['war'] += 2
            if subject in airforce_keywords:
                category_scores['airforce'] += 2
            if subject in nature_keywords:
                category_scores['nature'] += 1
            if subject in urban_keywords:
                category_scores['urban'] += 1
        
        # Return category with highest score
        max_category = max(category_scores, key=category_scores.get)
        if category_scores[max_category] > 0:
            return max_category
        
        return 'nature'  # Default fallback
    
    def generate_cinematic_scenes(self, prompt: str) -> List[Dict]:
        """
        Main method: Convert prompt into 3 cinematic scenes
        Each scene contains 4-6 visual nouns
        """
        print(f"\n🎬 Cinematic Prompt Engine")
        print(f"Input: '{prompt}'")
        
        # Extract subjects
        subjects = self.extract_key_subjects(prompt)
        print(f"Subjects: {subjects}")
        
        # Detect category
        category = self.detect_primary_category(subjects)
        print(f"Category: {category}")
        
        # Build visual vocabulary
        visual_elements = []
        for subject in subjects:
            visuals = self.convert_abstract_to_visual(subject)
            visual_elements.extend(visuals)
        
        # Remove duplicates while preserving order
        seen = set()
        visual_elements = [x for x in visual_elements if not (x in seen or seen.add(x))]
        
        print(f"Visual elements: {visual_elements[:12]}")
        
        # Generate 3 scenes
        scenes = []
        
        # Scene 1: Primary action with main subjects
        scene1_elements = []
        if category in self.scene_templates:
            # Use template as base
            template = self.scene_templates[category][0].split()
            scene1_elements.extend(template[:3])
        
        # Add specific visual elements
        scene1_elements.extend(visual_elements[:3])
        scene1_elements = list(dict.fromkeys(scene1_elements))[:6]  # Unique, max 6
        
        scene1 = {
            'id': 1,
            'query': ' '.join(scene1_elements),
            'keywords': scene1_elements,
            'duration': 4.0,
            'description': f"Primary: {' '.join(scene1_elements[:4])}"
        }
        scenes.append(scene1)
        
        # Scene 2: Secondary perspective
        scene2_elements = []
        if category in self.scene_templates and len(self.scene_templates[category]) > 1:
            template = self.scene_templates[category][1].split()
            scene2_elements.extend(template[:3])
        
        # Add different visual elements
        scene2_elements.extend(visual_elements[3:6])
        scene2_elements = list(dict.fromkeys(scene2_elements))[:6]
        
        scene2 = {
            'id': 2,
            'query': ' '.join(scene2_elements),
            'keywords': scene2_elements,
            'duration': 4.0,
            'description': f"Secondary: {' '.join(scene2_elements[:4])}"
        }
        scenes.append(scene2)
        
        # Scene 3: Contextual/atmospheric
        scene3_elements = []
        if category in self.scene_templates and len(self.scene_templates[category]) > 2:
            template = self.scene_templates[category][2].split()
            scene3_elements.extend(template[:3])
        
        # Add remaining visual elements
        scene3_elements.extend(visual_elements[6:9])
        scene3_elements = list(dict.fromkeys(scene3_elements))[:6]
        
        scene3 = {
            'id': 3,
            'query': ' '.join(scene3_elements),
            'keywords': scene3_elements,
            'duration': 4.0,
            'description': f"Context: {' '.join(scene3_elements[:4])}"
        }
        scenes.append(scene3)
        
        print(f"\nGenerated {len(scenes)} cinematic scenes:")
        for scene in scenes:
            print(f"  Scene {scene['id']}: {scene['query']}")
        
        return scenes
    
    def assess_prompt_quality(self, prompt: str) -> Tuple[bool, str]:
        """
        Assess if prompt is visually descriptive enough
        Returns: (is_good, feedback_message)
        """
        subjects = self.extract_key_subjects(prompt)
        
        # Check if prompt has enough visual nouns
        visual_count = 0
        for subject in subjects:
            if subject in self.visual_nouns or len(subject) > 4:
                visual_count += 1
        
        if visual_count < 2:
            return False, "Tip: Use visually descriptive prompts like 'military tanks moving through smoky battlefield at sunset'."
        
        # Check for too many abstract words
        abstract_words = {'struggle', 'dying', 'pain', 'fear', 'emotion', 'feeling'}
        abstract_count = sum(1 for word in subjects if word in abstract_words)
        
        if abstract_count > 2:
            return False, "Tip: Replace abstract concepts with visual elements (e.g., 'dying' → 'fallen soldiers ruins smoke')."
        
        return True, "Good prompt! Generating cinematic video..."


if __name__ == "__main__":
    # Test the engine
    engine = CinematicPromptEngine()
    
    test_prompts = [
        "A military tanker fighting with the air force army and soldiers dying",
        "beautiful sunset over mountains",
        "city traffic at night with lights"
    ]
    
    for prompt in test_prompts:
        print("\n" + "=" * 60)
        scenes = engine.generate_cinematic_scenes(prompt)
        is_good, feedback = engine.assess_prompt_quality(prompt)
        print(f"\nQuality: {is_good}")
        print(f"Feedback: {feedback}")
