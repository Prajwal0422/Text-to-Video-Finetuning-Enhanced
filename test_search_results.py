"""
Test what clips are actually found for specific prompts
"""

from backend.clip_fetcher import ClipFetcher

def test_search():
    fetcher = ClipFetcher()
    
    test_queries = [
        "two countries doing a war and soldiers struggling",
        "war soldiers military",
        "soldiers combat battle",
        "military troops action",
        "army soldiers fighting",
        "war zone conflict"
    ]
    
    print("=" * 60)
    print("Testing Pexels Search Results")
    print("=" * 60)
    
    for query in test_queries:
        print(f"\n\nQuery: '{query}'")
        print("-" * 60)
        
        videos = fetcher.search_videos(query, per_page=5)
        
        if videos:
            print(f"Found {len(videos)} videos:")
            for i, video in enumerate(videos[:3], 1):
                print(f"\n{i}. Video ID: {video.get('id')}")
                print(f"   Duration: {video.get('duration')}s")
                print(f"   User: {video.get('user', {}).get('name', 'Unknown')}")
                
                # Get video files
                video_files = video.get('video_files', [])
                if video_files:
                    best = max(video_files, key=lambda x: x.get('width', 0))
                    print(f"   Resolution: {best.get('width')}x{best.get('height')}")
                    print(f"   Size: {best.get('file_size', 0) / 1024 / 1024:.1f}MB")
        else:
            print("❌ No videos found")

if __name__ == "__main__":
    test_search()
