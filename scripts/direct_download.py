import os
import json
import subprocess
import re
import urllib.request
from typing import List, Dict, Optional

def clean_xml_srv1(text: str) -> str:
    """Удаляет XML теги из формата SRV1."""
    return re.sub(r'<[^>]*>', ' ', text).strip()

def get_subtitle_url(video_url: str) -> Optional[str]:
    try:
        cmd = ["yt-dlp", "--dump-json", video_url]
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        if result.returncode != 0:
            return None
        
        data = json.loads(result.stdout)
        subs = data.get('subtitles', {})
        auto_subs = data.get('automatic_captions', {})
        
        target = None
        if 'ru' in subs: target = subs['ru']
        elif 'ru' in auto_subs: target = auto_subs['ru']
        elif 'en' in subs: target = subs['en']
        elif 'en' in auto_subs: target = auto_subs['en']
        
        if target:
            # Предпочитаем srv1 (проще парсить) или vtt
            for fmt in target:
                if fmt.get('ext') == 'srv1': return fmt.get('url')
            for fmt in target:
                if fmt.get('ext') == 'vtt': return fmt.get('url')
            return target[0].get('url')
    except Exception:
        pass
    return None

def download_text(url: str) -> str:
    try:
        with urllib.request.urlopen(url) as response:
            text = response.read().decode('utf-8')
            return clean_xml_srv1(text)
    except Exception as e:
        return f"[Ошибка загрузки контента: {e}]"

def main():
    base_dir = "C:/ANTIGRAVITY/1"
    videos_list_path = os.path.join(base_dir, "videos_list.txt")
    
    if not os.path.exists(videos_list_path):
        print("videos_list.txt не найден")
        return

    with open(videos_list_path, 'r', encoding='utf-8') as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    
    videos = []
    for i in range(0, len(lines) - 1, 2):
        if 'youtube.com' in lines[i+1] or 'youtu.be' in lines[i+1]:
            videos.append({'title': lines[i], 'url': lines[i+1]})

    target_videos = videos[0:20]
    final_content = "# aiBoomb YouTube Channel Transcripts (Direct Load)\n\n"
    
    for idx, video in enumerate(target_videos, 1):
        print(f"[{idx}/{len(target_videos)}] {video['title']}...")
        sub_url = get_subtitle_url(video['url'])
        if sub_url:
            text = download_text(sub_url)
        else:
            text = "[Субтитры не найдены через Direct Load]"
        
        final_content += f"## {video['title']}\n**URL:** {video['url']}\n\n{text}\n\n---\n\n"

    out_file = os.path.join(base_dir, "aiBoomb_NotebookLM_Source.md")
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print(f"\nВСЁ! Файл готов: {out_file}")

if __name__ == "__main__":
    main()
