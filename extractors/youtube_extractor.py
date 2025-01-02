"""
YouTube content extractor that:
1. Downloads audio from YouTube videos
2. Transcribes the audio using Whisper
3. Caches transcriptions to avoid reprocessing
"""

from pytubefix import YouTube
import whisper
import subprocess
import os
from pathlib import Path
import json
import hashlib

class YouTubeExtractor:
    def __init__(self, url):
        """
        Initialize extractor with YouTube URL and setup cache directory.
        Also checks for FFmpeg installation which is required for audio processing.
        """
        self.url = url
        self.cache_dir = Path("cache")
        self.cache_dir.mkdir(exist_ok=True)
        
        if not self._check_ffmpeg():
            raise Exception("FFmpeg not found. Installation instructions provided...")
        
        self.model = whisper.load_model("tiny")
    
    def _check_ffmpeg(self):
        """Verify FFmpeg installation."""
        try:
            subprocess.run(['ffmpeg', '-version'], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
            return True
        except FileNotFoundError:
            return False
    
    def _get_cache_path(self):
        """Generate unique cache filename based on URL hash."""
        url_hash = hashlib.md5(self.url.encode()).hexdigest()
        return self.cache_dir / f"{url_hash}.json"
    
    def download_audio(self):
        """Download audio stream from YouTube video."""
        try:
            yt = YouTube(self.url)
            audio_stream = yt.streams.filter(only_audio=True).first()
            temp_dir = Path("temp")
            temp_dir.mkdir(exist_ok=True)
            temp_audio = temp_dir / "temp_audio.mp4"
            return audio_stream.download(filename=str(temp_audio))
            
        except Exception as e:
            raise Exception(f"Error downloading audio: {str(e)}")
    
    def transcribe(self):
        """
        Main transcription function that:
        1. Checks cache for existing transcription
        2. Downloads and transcribes if not cached
        3. Saves transcription to cache
        4. Cleans up temporary files
        """
        cache_path = self._get_cache_path()
        
        if cache_path.exists():
            with open(cache_path, 'r') as f:
                return json.load(f)['text']
        
        try:
            audio_path = self.download_audio()
            result = self.model.transcribe(
                audio_path,
                fp16=False,
                task='transcribe',
                language=None  # Auto-detect language
            )
            
            if os.path.exists(audio_path):
                os.remove(audio_path)
            
            with open(cache_path, 'w') as f:
                json.dump({'url': self.url, 'text': result["text"]}, f)
            
            return result["text"]
            
        except Exception as e:
            # Clean up on error
            temp_dir = Path("temp")
            if temp_dir.exists():
                for file in temp_dir.glob("*"):
                    file.unlink()
            raise e