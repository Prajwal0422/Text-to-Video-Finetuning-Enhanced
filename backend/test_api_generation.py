"""
Test API Video Generation
Tests the full system via the API endpoint
"""

import asyncio
import websockets
import json
import sys

async def test_generation():
    uri = "ws://localhost:8000/ws/generate"
    
    print("=" * 60)
    print("TESTING API VIDEO GENERATION")
    print("=" * 60)
    print(f"Connecting to: {uri}")
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Connected to WebSocket")
            
            # Send generation request
            prompt = "A beautiful sunset over mountains"
            request = {
                "prompt": prompt
            }
            
            print(f"\n📝 Sending prompt: '{prompt}'")
            await websocket.send(json.dumps(request))
            print("✅ Request sent")
            
            print("\n" + "-" * 60)
            print("GENERATION PROGRESS")
            print("-" * 60)
            
            # Receive messages
            video_path = None
            
            while True:
                try:
                    message = await websocket.recv()
                    data = json.loads(message)
                    
                    msg_type = data.get('type')
                    
                    if msg_type == 'progress':
                        progress = data.get('progress', 0)
                        message_text = data.get('message', '')
                        print(f"[{progress:3d}%] {message_text}")
                    
                    elif msg_type == 'complete':
                        video_path = data.get('video_path')
                        duration = data.get('duration', 0)
                        message_text = data.get('message', '')
                        
                        print("-" * 60)
                        print(f"✅ {message_text}")
                        print(f"📹 Video: {video_path}")
                        print(f"⏱️  Time: {duration:.1f}s")
                        break
                    
                    elif msg_type == 'error':
                        error_msg = data.get('message', 'Unknown error')
                        print("-" * 60)
                        print(f"❌ Error: {error_msg}")
                        return False
                
                except websockets.exceptions.ConnectionClosed:
                    print("Connection closed")
                    break
            
            if video_path:
                print("\n" + "=" * 60)
                print("✅ VIDEO GENERATION SUCCESS")
                print("=" * 60)
                print(f"Video URL: http://localhost:8000{video_path}")
                print(f"Local path: backend/{video_path}")
                print("=" * 60)
                return True
            else:
                print("\n❌ No video path received")
                return False
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\nMake sure the server is running: python main.py\n")
    
    try:
        result = asyncio.run(test_generation())
        
        if result:
            print("\n✅ API TEST PASSED")
            sys.exit(0)
        else:
            print("\n❌ API TEST FAILED")
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\n❌ Aborted by user")
        sys.exit(1)
