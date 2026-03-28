"""
Prompt Optimization Engine
Enhances user prompts for better video generation results
"""

import re
from typing import List, Dict, Tuple

class PromptOptimizer:
    def __init__(self):
        # Quality enhancers
        self.quality_keywords = [
            'high quality', 'cinematic', 'professional', 'detailed',
            'sharp', 'clear', 'vivid', 'stunning'
        ]
        
        # Scene descriptors
        self.scene_descriptors = {
            'nature': ['natural', 'outdoor', 'scenic', 'landscape'],
            'urban': ['city', 'urban', 'street', 'downtown'],
            'action': ['dynamic', 'motion', 'fast', 'energetic'],
            'calm': ['peaceful', 'serene', 'tranquil', 'gentle']
        }
        
        # Lighting keywords
        self.lighting_terms = [
            'golden hour', 'sunset', 'sunrise', 'daylight',
            'dramatic lighting', 'soft light', 'natural light'
        ]
        
        # Camera movements
        self.camera_movements = [
            'smooth pan', 'slow zoom', 'aerial view', 'tracking shot',
            'steady cam', 'dolly shot'
        ]
    
    def optimize(self, prompt: str) -> str:
        """Optimize a prompt for better results"""
        # Clean prompt
        prompt = self._clean_prompt(prompt)
        
        # Enhance with quality keywords if missing
        prompt = self._add_quality_keywords(prompt)
        
        # Add scene context
        prompt = self._add_scene_context(prompt)
        
        # Ensure proper length
        prompt = self._optimize_length(prompt)
        
        return prompt
    
    def _clean_prompt(self, prompt: str) -> str:
        """Clean and normalize prompt"""
        # Remove extra whitespace
        prompt = ' '.join(prompt.split())
        
        # Remove special characters
        prompt = re.sub(r'[^\w\s,.-]', '', prompt)
        
        # Lowercase
        prompt = prompt.lower()
        
        return prompt.strip()
    
    def _add_quality_keywords(self, prompt: str) -> str:
        """Add quality enhancers if missing"""
        # Check if already has quality keywords
        has_quality = any(kw in prompt.lower() for kw in self.quality_keywords)
        
        if not has_quality:
            # Add cinematic quality
            prompt = f"cinematic {prompt}"
        
        return prompt
    
    def _add_scene_context(self, prompt: str) -> str:
        """Add scene descriptors based on content"""
        prompt_lower = prompt.lower()
        
        # Detect scene type
        for scene_type, descriptors in self.scene_descriptors.items():
            if any(desc in prompt_lower for desc in descriptors):
                # Scene type detected, check if needs enhancement
                if 'view' not in prompt_lower and 'shot' not in prompt_lower:
                    prompt = f"{prompt}, wide angle view"
                break
        
        return prompt
    
    def _optimize_length(self, prompt: str, min_words: int = 3, max_words: int = 15) -> str:
        """Ensure prompt is optimal length"""
        words = prompt.split()
        
        if len(words) < min_words:
            # Too short, add context
            prompt = f"{prompt}, high quality video"
        elif len(words) > max_words:
            # Too long, truncate
            prompt = ' '.join(words[:max_words])
        
        return prompt
    
    def generate_variations(self, prompt: str, count: int = 3) -> List[str]:
        """Generate prompt variations for better results"""
        base_prompt = self._clean_prompt(prompt)
        variations = [base_prompt]
        
        # Variation 1: Add lighting
        if not any(term in base_prompt for term in self.lighting_terms):
            variations.append(f"{base_prompt}, golden hour lighting")
        
        # Variation 2: Add camera movement
        if not any(move in base_prompt for move in self.camera_movements):
            variations.append(f"{base_prompt}, smooth camera movement")
        
        # Variation 3: Add quality emphasis
        variations.append(f"professional {base_prompt}, 4k quality")
        
        return variations[:count]
    
    def extract_keywords(self, prompt: str) -> List[str]:
        """Extract key search terms from prompt"""
        # Clean prompt
        prompt = self._clean_prompt(prompt)
        
        # Remove common words
        stop_words = {'a', 'an', 'the', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        
        words = prompt.split()
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        
        # Limit to top 5 keywords
        return keywords[:5]
    
    def score_prompt(self, prompt: str) -> Dict:
        """Score prompt quality"""
        score = 0
        feedback = []
        
        # Length check
        word_count = len(prompt.split())
        if 3 <= word_count <= 15:
            score += 30
            feedback.append("✅ Good length")
        else:
            feedback.append("⚠️  Length could be improved")
        
        # Quality keywords
        has_quality = any(kw in prompt.lower() for kw in self.quality_keywords)
        if has_quality:
            score += 25
            feedback.append("✅ Has quality keywords")
        else:
            feedback.append("⚠️  Missing quality keywords")
        
        # Specificity
        if ',' in prompt or len(prompt.split()) >= 5:
            score += 25
            feedback.append("✅ Specific description")
        else:
            feedback.append("⚠️  Could be more specific")
        
        # Scene context
        has_scene = any(
            any(desc in prompt.lower() for desc in descriptors)
            for descriptors in self.scene_descriptors.values()
        )
        if has_scene:
            score += 20
            feedback.append("✅ Clear scene context")
        else:
            feedback.append("⚠️  Scene context unclear")
        
        return {
            'score': score,
            'grade': self._get_grade(score),
            'feedback': feedback,
            'optimized': self.optimize(prompt)
        }
    
    def _get_grade(self, score: int) -> str:
        """Convert score to grade"""
        if score >= 80:
            return 'A'
        elif score >= 60:
            return 'B'
        elif score >= 40:
            return 'C'
        else:
            return 'D'
    
    def analyze_prompt(self, prompt: str) -> str:
        """Generate detailed prompt analysis"""
        analysis = self.score_prompt(prompt)
        
        report = []
        report.append("=" * 60)
        report.append("PROMPT ANALYSIS")
        report.append("=" * 60)
        report.append(f"Original: {prompt}")
        report.append(f"Score: {analysis['score']}/100 (Grade: {analysis['grade']})")
        report.append("")
        report.append("Feedback:")
        for item in analysis['feedback']:
            report.append(f"  {item}")
        report.append("")
        report.append(f"Optimized: {analysis['optimized']}")
        report.append("=" * 60)
        
        return "\n".join(report)


# Global instance
optimizer = PromptOptimizer()


if __name__ == "__main__":
    print("Prompt Optimizer Test")
    print("=" * 60)
    
    # Test prompts
    test_prompts = [
        "ocean",
        "beautiful sunset over mountains",
        "fast car racing through city streets at night",
        "a very long prompt that goes on and on with too many words and details that might not be necessary"
    ]
    
    for prompt in test_prompts:
        print(f"\nOriginal: {prompt}")
        optimized = optimizer.optimize(prompt)
        print(f"Optimized: {optimized}")
        
        score = optimizer.score_prompt(prompt)
        print(f"Score: {score['score']}/100 (Grade: {score['grade']})")
        print()
