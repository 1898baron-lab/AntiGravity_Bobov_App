import subprocess
import json
import os

def get_channel_videos(channel_url, max_videos=20):
    cmd = [
        "yt-dlp",
        "--dump-json",
        "--flat-playlist",
        "--playlist-end", str(max_videos),
        channel_url
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        videos = []
        for line in result.stdout.strip().split('\n'):
            if line:
                data = json.loads(line)
                # YouTube sometimes returns "url" as just "/watch?v=...", sometimes a full URL.
                url = data.get("url", "")
                if url and url.startswith("/"):
                    url = f"https://www.youtube.com{url}"
                elif url and not url.startswith("http"):
                    url = f"https://www.youtube.com/watch?v={data.get('id')}"
                videos.append({
                    "title": data.get("title", "No Title"),
                    "url": url
                })
        return videos
    except Exception as e:
        print(f"Error extracting videos: {e}")
        return []

if __name__ == "__main__":
    channel_url = "https://www.youtube.com/@aiBoomb"
    print(f"Fetching {channel_url}...")
    videos = get_channel_videos(channel_url, 20)
    
    out_file = "videos_list.txt"
    with open(out_file, "w", encoding="utf-8") as f:
        for i, v in enumerate(videos, 1):
            f.write(f"{i}. {v['title']}\n{v['url']}\n\n")
    
    print(f"Saved {len(videos)} videos to {os.path.abspath(out_file)}")
