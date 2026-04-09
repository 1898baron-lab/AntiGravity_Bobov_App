import sys
import requests
import re
from youtube_transcript_api import YouTubeTranscriptApi

def get_video_title(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers)
        match = re.search(r'<title>(.*?)</title>', r.text)
        if match:
            return match.group(1).replace(" - YouTube", "").strip()
        return f"Video {video_id}"
    except:
        return f"Video {video_id}"

def get_transcript(video_id):
    try:
        api = YouTubeTranscriptApi()
        # Пробуем русский, если нет - первый попавшийся
        try:
            fetched = api.fetch(video_id, languages=['ru'])
        except:
            fetched = api.fetch(video_id)
            
        text = ' '.join([s.text if hasattr(s, 'text') else (s.get('text', '') if isinstance(s, dict) else str(s)) for s in fetched])
        return re.sub(r'\s+', ' ', text).strip()
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    v_id = "JtjfYS9hfWw"
    title = get_video_title(v_id)
    text = get_transcript(v_id)
    
    sys.stdout.reconfigure(encoding='utf-8')
    print(f"=== Видео: {title} ===")
    print(text)
    print("\n")
