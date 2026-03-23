"""
Prompt Enhancer
Improves user prompts for better video generation results
"""

import re
from typing import List, Dict, Tuple

class PromptEnhancer:
    """Enhances user prompts with cinematic details and keywords"""
    
    # Cinematic enhancement templates
    CINEMATIC_STYLES = {
        'nature': ['cinematic', 'beautiful', 'scenic', 'breathtaking', 'majestic'],
        'urban': ['modern', 'vibrant', 'dynamic', 'bustling', 'contemporary'],
        'action': ['intense', 'dramatic', 'powerful', 'energetic', 'fast-paced'],
        'calm': ['peaceful', 'serene', 'tranquil', 'gentle', 'soothing']
    }
    
    # Quality enhancers
    QUALITY_TERMS = [
        'high quality', 'professional', 'cinematic', '4k', 'detailed',
        'sharp focus', 'well-lit', 'vivid colors'
    ]
    
    # Camera movements
    CAMERA_MOVEMENTS = [
        'smooth pan', 'slow zoom', 'tracking shot', 'aerial view',
        'close-up', 'wide angle', 'establishing shot'
    ]
    
    def __init__(self):
        self.enhancement_history = []
    
    def detect_theme(self, prompt: str) -> str:
        """Detect the theme of the prompt"""
        prompt_lower = prompt.lower()
        
        nature_keywords = ['nature', 'landscape', 'mountain', 'ocean', 'forest', 'sunset', 'beach', 'sky']
        urban_keywords = ['city', 'urban', 'street', 'building', 'downtown', 'traffic', 'lights']
        action_keywords = ['action', 'fast', 'racing', 'sport', 'fight', 'chase', 'running', 'jumping']
        calm_keywords = ['calm', 'peaceful', 'quiet', 'meditation', 'zen', 'relaxing']
        
        if any(kw in prompt_lower for kw in nature_keywords):
            return 'nature'
        elif any(kw in prompt_lower for kw in urban_keywords):
            return 'urban'
        elif any(kw in prompt_lower for kw in action_keywords):
            return 'action'
        elif any(kw in prompt_lower for kw in calm_keywords):
            return 'calm'
        
        return 'general'
    
    def add_cinematic_style(self, prompt: str, theme: str) -> str:
        """Add cinematic style descriptors"""
        if theme in self.CINEMATIC_STYLES:
            styles = self.CINEMATIC_STYLES[theme]
            # Add 1-2 style descriptors
            style_text = ', '.join(styles[:2])
            return f"{style_text} {prompt}"
        return prompt
    
    def add_quality_terms(self, prompt: str) -> str:
        """Add quality enhancement terms"""
        # Check if quality terms already present
        prompt_lower = prompt.lower()
        has_quality = any(term in prompt_lower for term in ['quality', 'cinematic', '4k', 'hd'])
        
        if not has_quality:
            return f"{prompt}, high quality, cinematic"
        return prompt
    
    def add_camera_movement(self, prompt: str, theme: str) -> str:
        """Add appropriate camera movement"""
        prompt_lower = prompt.lower()
        has_camera = any(term in prompt_lower for term in ['pan', 'zoom', 'shot', 'view', 'angle'])
        
        if not has_camera:
            if theme == 'nature':
                return f"{prompt}, slow pan"
            elif theme == 'urban':
                return f"{prompt}, tracking shot"
            elif theme == 'action':
                return f"{prompt}, dynamic camera"
        
        return prompt
    
    def expand_short_prompt(self, prompt: str) -> str:
        """Expand very short prompts with context"""
        words = prompt.split()
        
        if len(words) <= 2:
            # Very short prompt, add context
            theme = self.detect_theme(prompt)
            
            if theme == 'nature':
                return f"{prompt} in beautiful natural environment, scenic view"
            elif theme == 'urban':
                return f"{prompt} in modern city, urban landscape"
            elif theme == 'action':
                return f"{prompt} with dynamic movement, energetic scene"
            else:
                return f"{prompt}, cinematic scene"
        
        return prompt
    
    def remove_redundancy(self, prompt: str) -> str:
        """Remove redundant words and phrases"""
        # Remove duplicate words
        words = prompt.split()
        seen = set()
        unique_words = []
        
        for word in words:
            word_lower = word.lower().strip('.,')
            if word_lower not in seen:
                seen.add(word_lower)
                unique_words.append(word)
        
        return ' '.join(unique_words)
    
    def enhance(
        self,
        prompt: str,
        add_style: bool = True,
        add_quality: bool = True,
        add_camera: bool = False,
        expand_short: bool = True
    ) -> Dict[str, str]:
        """
        Enhance a prompt with cinematic details
        
        Args:
            prompt: Original user prompt
            add_style: Add cinematic style descriptors
            add_quality: Add quality terms
            add_camera: Add camera movement
            expand_short: Expand very short prompts
        
        Returns:
            Dictionary with original and enhanced prompts
        """
        original = prompt.strip()
        enhanced = original
        
        # Detect theme
        theme = self.detect_theme(enhanced)
        
        # Expand if too short
        if expand_short:
            enhanced = self.expand_short_prompt(enhanced)
        
        # Add cinematic style
        if add_style:
            enhanced = self.add_cinematic_style(enhanced, theme)
        
        # Add quality terms
        if add_quality:
            enhanced = self.add_quality_terms(enhanced)
        
        # Add camera movement
        if add_camera:
            enhanced = self.add_camera_movement(enhanced, theme)
        
        # Remove redundancy
        enhanced = self.remove_redundancy(enhanced)
        
        # Store in history
        self.enhancement_history.append({
            'original': original,
            'enhanced': enhanced,
            'theme': theme
        })
        
        return {
            'original': original,
            'enhanced': enhanced,
            'theme': theme,
            'improvements': self._list_improvements(original, enhanced)
        }
    
    def _list_improvements(self, original: str, enhanced: str) -> List[str]:
        """List what improvements were made"""
        improvements = []
        
        if len(enhanced) > len(original):
            improvements.append('Added descriptive details')
        
        if 'cinematic' in enhanced.lower() and 'cinematic' not in original.lower():
            improvements.append('Added cinematic quality')
        
        if any(style in enhanced.lower() for style in ['beautiful', 'scenic', 'majestic']):
            improvements.append('Added style descriptors')
        
        if any(cam in enhanced.lower() for cam in ['pan', 'zoom', 'shot']):
            improvements.append('Added camera movement')
        
        return improvements
    
    def get_suggestions(self, prompt: str) -> List[str]:
        """Get alternative prompt suggestions"""
        theme = self.detect_theme(prompt)
        suggestions = []
        
        # Generate 3 variations
        suggestions.append(self.enhance(prompt, add_style=True, add_quality=True, add_camera=False)['enhanced'])
        suggestions.append(self.enhance(prompt, add_style=True, add_quality=True, add_camera=True)['enhanced'])
        suggestions.append(self.enhance(prompt, add_style=False, add_quality=True, add_camera=True)['enhanced'])
        
        return list(set(suggestions))  # Remove duplicates


# Example usage
if __name__ == "__main__":
    enhancer = PromptEnhancer()
    
    test_prompts = [
        "ocean waves",
        "city at night",
        "mountain landscape",
        "fast car racing"
    ]
    
    print("=" * 60)
    print("PROMPT ENHANCER - TEST")
    print("=" * 60)
    
    for prompt in test_prompts:
        print(f"\nOriginal: '{prompt}'")
        result = enhancer.enhance(prompt)
        print(f"Enhanced: '{result['enhanced']}'")
        print(f"Theme: {result['theme']}")
        print(f"Improvements: {', '.join(result['improvements'])}")
