"""
Test the fixed prompt processing
"""

from backend.visual_intent_mapper import VisualIntentMapper

def test_prompt_mapping():
    mapper = VisualIntentMapper()
    
    test_prompts = [
        "two countries doing a war and soldiers struggling to live",
        "beautiful sunset over mountains",
        "ocean waves at sunset",
        "busy city traffic at night"
    ]
    
    for prompt in test_prompts:
        print("\n" + "=" * 60)
        print(f"Testing: {prompt}")
        print("=" * 60)
        
        scenes = mapper.map_prompt_to_scenes(prompt)
        
        print(f"\nGenerated {len(scenes)} scenes:")
        for scene in scenes:
            print(f"\nScene {scene['id']}:")
            print(f"  Query: {scene['query']}")
            print(f"  Keywords: {scene['keywords']}")
            if 'alternative_queries' in scene:
                print(f"  Alternative queries: {len(scene['alternative_queries'])}")

if __name__ == "__main__":
    test_prompt_mapping()
