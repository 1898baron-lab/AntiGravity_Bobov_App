import youtube_transcript_api
from youtube_transcript_api import YouTubeTranscriptApi
import sys

print(f"Python version: {sys.version}")
print(f"Module file: {youtube_transcript_api.__file__}")
print(f"YouTubeTranscriptApi type: {type(YouTubeTranscriptApi)}")
print(f"YouTubeTranscriptApi dir: {dir(YouTubeTranscriptApi)}")

try:
    # Try calling it
    print("Testing get_transcript call...")
    # Just a dummy ID to see if the method exists
    # If it raises a 'not found' error from YouTube, the method exists!
    YouTubeTranscriptApi.get_transcript("abc", languages=['en'])
except Exception as e:
    print(f"Call resulted in: {type(e).__name__}: {e}")
