"""
NEXUS VISION - Visual Intent Mapper
Converts complex prompts into cinematic visual search queries
Handles semantic expansion for better stock footage matching
"""

import re
from typing import List, Dict, Set, Tuple

class VisualIntentMapper:
    def __init__(self):
        # Semantic expansion database
        self.semantic_expansions = {
            # War & Military - IMPROVED
            'war': ['war military combat', 'soldiers battle action', 'military conflict warfare', 
                   'army troops fighting', 'combat zone battlefield'],
            'battle': ['soldiers fighting combat', 'military action warfare', 'battlefield smoke fire',
                      'army troops conflict', 'war zone destruction'],
            'soldiers': ['military troops uniform', 'army soldiers combat', 'soldiers marching training',
                        'military forces action', 'troops battlefield war'],
            'military': ['army forces vehicles', 'military training exercise', 'soldiers uniform march',
                        'defense forces action', 'military base operations'],
            'combat': ['military combat action', 'soldiers fighting battle', 'combat warfare troops',
                      'military action combat', 'battle combat soldiers'],
            'army': ['military army troops', 'soldiers army uniform', 'army forces military',
                    'military personnel army', 'army soldiers marching'],
            'conflict': ['military conflict war', 'soldiers conflict battle', 'war conflict troops',
                        'military action conflict', 'conflict warfare soldiers'],
            'struggling': ['difficult challenge effort', 'hardship adversity tough', 'struggle survival action',
                          'challenging difficult scene', 'effort struggle motion'],
            
            # Nature & Landscapes
            'sunset': ['golden hour sky clouds', 'sunset horizon landscape', 'evening sky colors',
                      'dusk atmosphere scenic', 'sunset ocean beach'],
            'mountains': ['mountain peaks landscape', 'alpine scenery nature', 'mountain range vista',
                         'rocky peaks summit', 'mountain valley scenic'],
            'ocean': ['sea waves water', 'ocean coast beach', 'blue water horizon',
                     'ocean waves crashing', 'seascape water motion'],
            'forest': ['trees woodland nature', 'forest landscape green', 'dense trees vegetation',
                      'forest path scenic', 'woodland environment'],
            
            # Urban & City
            'city': ['urban skyline buildings', 'city streets traffic', 'downtown metropolitan',
                    'city lights night', 'urban landscape architecture'],
            'traffic': ['cars highway road', 'vehicles busy street', 'traffic jam congestion',
                       'highway cars moving', 'urban traffic flow'],
            'street': ['city street urban', 'road vehicles traffic', 'downtown street scene',
                      'urban street life', 'street view city'],
            
            # Action & Motion
            'running': ['person running motion', 'athlete running fast', 'running action sport',
                       'people running outdoor', 'runner motion speed'],
            'flying': ['aerial flight sky', 'bird flying motion', 'drone aerial view',
                      'flying movement air', 'flight sky clouds'],
            'driving': ['car driving road', 'vehicle motion highway', 'driving street urban',
                       'car moving traffic', 'driving action speed'],
            
            # Weather & Atmosphere
            'rain': ['rainfall water drops', 'rainy weather storm', 'rain falling motion',
                    'wet rain atmosphere', 'rainfall clouds sky'],
            'storm': ['stormy clouds sky', 'storm weather dramatic', 'lightning storm dark',
                     'storm clouds rain', 'stormy atmosphere'],
            'clouds': ['sky clouds atmosphere', 'cloudy sky weather', 'clouds moving timelapse',
                      'cloud formation sky', 'dramatic clouds'],
            
            # People & Lifestyle
            'people': ['crowd urban street', 'people walking city', 'group activity outdoor',
                      'people lifestyle scene', 'crowd motion busy'],
            'crowd': ['people group busy', 'crowd urban street', 'many people gathering',
                     'crowd motion city', 'busy crowd scene'],
            'walking': ['person walking street', 'people walking urban', 'walking motion outdoor',
                       'pedestrian walking city', 'walking action movement'],
            
            # Technology & Modern
            'technology': ['modern tech digital', 'technology innovation future', 'tech devices screen',
                          'digital technology modern', 'technology concept abstract'],
            'computer': ['technology screen digital', 'computer work office', 'tech device modern',
                        'computer screen display', 'digital computer tech'],
            
            # Abstract & Concepts
            'struggle': ['difficult challenge effort', 'hardship adversity tough', 'struggle effort action',
                        'challenging difficult scene', 'effort struggle motion'],
            'conflict': ['tension confrontation clash', 'conflict struggle action', 'opposing forces battle',
                        'conflict scene dramatic', 'confrontation tension'],
            'survival': ['endurance perseverance tough', 'survival challenge harsh', 'surviving difficult',
                        'survival action extreme', 'endurance survival scene'],
            
            # Additional expansions for better coverage
            'beautiful': ['scenic stunning gorgeous', 'beautiful landscape nature', 'aesthetic pleasing view',
                         'beautiful scenery picturesque', 'gorgeous beautiful scene'],
            'fast': ['speed motion quick', 'fast moving rapid', 'quick action speed',
                    'fast motion blur', 'rapid fast movement'],
            'slow': ['slow motion gentle', 'calm peaceful slow', 'slow movement smooth',
                    'gentle slow motion', 'slow peaceful scene'],
            'happy': ['joyful cheerful positive', 'happy people smiling', 'celebration joy happy',
                     'happy mood positive', 'cheerful happy scene'],
            'sad': ['melancholy emotional somber', 'sad mood atmosphere', 'emotional sad scene',
                   'somber sad mood', 'sad emotional moment']
        }
        
        # Fallback themes for when no matches found
        self.fallback_themes = {
            'military': ['military training exercise', 'army vehicles convoy', 'soldiers marching'],
            'nature': ['nature landscape scenic', 'natural environment outdoor', 'wilderness scenic'],
            'urban': ['city urban street', 'downtown buildings', 'urban landscape'],
            'action': ['motion movement dynamic', 'action scene dramatic', 'fast motion'],
            'dramatic': ['dramatic sky clouds', 'intense atmosphere', 'dramatic lighting']
        }
        
        # Context categories
        self.context_categories = {
            'military': ['war', 'battle', 'soldiers', 'army', 'military', 'combat', 'troops', 'conflict'],
            'nature': ['sunset', 'mountains', 'ocean', 'forest', 'landscape', 'scenic', 'natural'],
            'urban': ['city', 'traffic', 'street', 'urban', 'downtown', 'buildings'],
            'action': ['running', 'flying', 'driving', 'moving', 'fast', 'motion'],
            'weather': ['rain', 'storm', 'clouds', 'sky', 'weather'],
            'people': ['people', 'crowd', 'person', 'walking', 'group']
        }
    
    def detect_primary_theme(self, prompt: str) -> str:
        """Detect the primary theme/category of the prompt"""
        prompt_lower = prompt.lower()
        
        theme_scores = {}
        for theme, keywords in self.context_categories.items():
            score = sum(1 for keyword in keywords if keyword in prompt_lower)
            if score > 0:
                theme_scores[theme] = score
        
        if theme_scores:
            return max(theme_scores, key=theme_scores.get)
        
        return 'nature'  # Default fallback
    
    def extract_key_concepts(self, prompt: str) -> List[str]:
        """Extract key concepts from prompt"""
        # Remove common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                     'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
                     'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
                     'should', 'could', 'may', 'might', 'must', 'can', 'that', 'this'}
        
        # Extract words
        words = re.findall(r'\b[a-z]+\b', prompt.lower())
        
        # Filter and return meaningful words
        concepts = [w for w in words if w not in stop_words and len(w) > 3]
        
        return concepts[:10]  # Limit to top 10
    
    def expand_concept(self, concept: str) -> List[str]:
        """Expand a single concept into visual search queries"""
        # Direct match
        if concept in self.semantic_expansions:
            return self.semantic_expansions[concept]
        
        # Partial match
        for key, expansions in self.semantic_expansions.items():
            if concept in key or key in concept:
                return expansions
        
        # No match - return concept with generic modifiers
        return [
            f"{concept} scene dramatic",
            f"{concept} action motion",
            f"{concept} cinematic view"
        ]
    
    def generate_visual_queries(self, prompt: str, max_queries: int = 5) -> List[str]:
        """
        Main method: Convert prompt into 5 semantic visual search queries
        FIXED: Now keeps original prompt as primary query
        
        Args:
            prompt: User's text prompt
            max_queries: Maximum number of queries to generate (default 5)
        
        Returns:
            List of visual search query strings
        """
        print(f"\n🎬 Visual Intent Mapping")
        print(f"Prompt: '{prompt}'")
        
        # Detect primary theme
        primary_theme = self.detect_primary_theme(prompt)
        print(f"Primary theme: {primary_theme}")
        
        # Extract key concepts
        concepts = self.extract_key_concepts(prompt)
        print(f"Key concepts: {concepts}")
        
        # Generate queries
        queries = []
        used_queries = set()
        
        # FIRST: Add the original prompt as the primary query
        # This ensures we search for exactly what the user asked for
        original_query = ' '.join(prompt.lower().split()[:8])  # Use first 8 words
        queries.append(original_query)
        used_queries.add(original_query)
        print(f"Primary query: '{original_query}'")
        
        # SECOND: Add concept-based variations for better coverage
        for concept in concepts[:2]:  # Use top 2 concepts
            expansions = self.expand_concept(concept)
            for expansion in expansions[:2]:  # Take first 2 expansions per concept
                if expansion not in used_queries and len(queries) < max_queries:
                    queries.append(expansion)
                    used_queries.add(expansion)
        
        # THIRD: Add keyword combinations from the original prompt
        if len(concepts) >= 2 and len(queries) < max_queries:
            keyword_combo = ' '.join(concepts[:3])
            if keyword_combo not in used_queries:
                queries.append(keyword_combo)
                used_queries.add(keyword_combo)
        
        # FOURTH: If not enough queries, add fallback based on theme
        if len(queries) < max_queries and primary_theme in self.fallback_themes:
            fallbacks = self.fallback_themes[primary_theme]
            for fallback in fallbacks:
                if fallback not in used_queries and len(queries) < max_queries:
                    queries.append(fallback)
                    used_queries.add(fallback)
        
        # Limit to max_queries
        queries = queries[:max_queries]
        
        print(f"Generated {len(queries)} visual queries:")
        for i, query in enumerate(queries, 1):
            print(f"  {i}. '{query}'")
        
        return queries
    
    def map_prompt_to_scenes(self, prompt: str) -> List[Dict]:
        """
        Convert prompt into scene objects with visual queries
        FIXED: Now uses original prompt as primary query
        
        Returns:
            List of scene dictionaries with visual queries
        """
        # Generate visual queries (first one is the original prompt)
        visual_queries = self.generate_visual_queries(prompt, max_queries=5)
        
        # Create scenes (use first 3 queries for 3 scenes)
        scenes = []
        for i, query in enumerate(visual_queries[:3], 1):
            # For the first scene, use the full original prompt
            if i == 1:
                scene_query = prompt  # Use full original prompt
                keywords = self.extract_key_concepts(prompt)[:5]
            else:
                scene_query = query
                keywords = query.split()[:4]
            
            scene = {
                'id': i,
                'query': scene_query,
                'keywords': keywords,
                'duration': 4.0,  # 4 seconds per scene
                'description': f"Scene {i}: {scene_query}"
            }
            scenes.append(scene)
        
        # Store remaining queries for multi-query search
        if len(visual_queries) > 3:
            for scene in scenes:
                scene['alternative_queries'] = visual_queries[3:]
        
        return scenes


if __name__ == "__main__":
    # Test the mapper
    mapper = VisualIntentMapper()
    
    test_prompts = [
        "two countries doing a war and soldiers struggling to live",
        "beautiful sunset over mountains",
        "busy city traffic at night",
        "people walking in crowded street"
    ]
    
    for prompt in test_prompts:
        print("\n" + "=" * 60)
        scenes = mapper.map_prompt_to_scenes(prompt)
        print(f"\nGenerated {len(scenes)} scenes")
        for scene in scenes:
            print(f"  Scene {scene['id']}: {scene['query']}")
