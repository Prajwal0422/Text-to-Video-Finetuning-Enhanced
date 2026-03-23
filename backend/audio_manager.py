"""
Audio Manager
Manages audio tracks and background music for videos
"""

import os
from typing import Optional, List
from moviepy import AudioFileClip, CompositeAudioClip
import requests

class AudioManager:
    """Manages audio for video generation"""
    
    def __init__(self, audio_dir: str = "outputs/audio"):
        self.audio_dir = audio_dir
        os.makedirs(audio_dir, exist_ok=True)
        
        # Default audio library
        self.audio_library = {
            'calm': 'https://example.com/calm.mp3',
            'energetic': 'https://example.com/energetic.mp3',
            'cinematic': 'https://example.com/cinematic.mp3',
            'ambient': 'https://example.com/ambient.mp3'
        }
    
    def download_audio(self, url: str, filename: str) -> str:
        """Download audio file"""
        filepath = os.path.join(self.audio_dir, filename)
        
        if os.path.exists(filepath):
            return filepath
        
        response = requests.get(url, stream=True)
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return filepath
    
    def add_background_music(
        self,
        video_path: str,
        audio_type: str = 'ambient',
        volume: float = 0.3
    ) -> str:
        """Add background music to video"""
        from moviepy import VideoFileClip
        
        # Load video
        video = VideoFileClip(video_path)
        
        # Get audio file
        if audio_type in self.audio_library:
            audio_url = self.audio_library[audio_type]
            audio_path = self.download_audio(audio_url, f"{audio_type}.mp3")
        else:
            raise ValueError(f"Unknown audio type: {audio_type}")
        
        # Load audio
        audio = AudioFileClip(audio_path)
        
        # Loop audio to match video duration
        if audio.duration < video.duration:
            loops = int(video.duration / audio.duration) + 1
            audio = CompositeAudioClip([audio] * loops).subclip(0, video.duration)
        else:
            audio = audio.subclip(0, video.duration)
        
        # Adjust volume
        audio = audio.volumex(volume)
        
        # Add to video
        video = video.set_audio(audio)
        
        # Export
        output_path = video_path.replace('.mp4', '_with_audio.mp4')
        video.write_videofile(output_path, codec='libx264', audio_codec='aac')
        
        video.close()
        audio.close()
        
        return output_path
    
    def add_voiceover(
        self,
        video_path: str,
        voiceover_text: str,
        voice: str = 'en-US-Standard-A'
    ) -> str:
        """Add AI voiceover to video"""
        # Placeholder for TTS integration
        print(f"Voiceover: {voiceover_text}")
        return video_path
    
    def mix_audio_tracks(
        self,
        tracks: List[tuple],
        output_filename: str
    ) -> str:
        """Mix multiple audio tracks"""
        audio_clips = []
        
        for track_path, volume in tracks:
            audio = AudioFileClip(track_path)
            audio = audio.volumex(volume)
            audio_clips.append(audio)
        
        mixed = CompositeAudioClip(audio_clips)
        
        output_path = os.path.join(self.audio_dir, output_filename)
        mixed.write_audiofile(output_path)
        
        return output_path


if __name__ == "__main__":
    print("Audio Manager - Ready for audio processing")
