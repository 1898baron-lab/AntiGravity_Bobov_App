import os
import re
from typing import List, Dict, Any, Optional

# Сверхстабильный импорт
try:
    import youtube_transcript_api
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    youtube_transcript_api = None
    YouTubeTranscriptApi = None

def get_video_id(url: str) -> Optional[str]:
    patterns = [
        r"(?:v=|\/)([0-9A-Za-z_-]{11}).*",
        r"youtu\.be\/([0-9A-Za-z_-]{11})",
        r"shorts\/([0-9A-Za-z_-]{11})"
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def fetch_transcript_api(video_id: str) -> str:
    """Универсальный фетчер с перебором методов."""
    if not youtube_transcript_api:
        return "[Ошибка: Библиотека не установлена]"
    
    # Список мест, где может лежать нужный метод
    possibilities = [
        YouTubeTranscriptApi,
        getattr(youtube_transcript_api, 'YouTubeTranscriptApi', None),
        youtube_transcript_api
    ]

    for api in possibilities:
        if api and hasattr(api, 'get_transcript'):
            try:
                # Пробуем RU, потом EN
                data = api.get_transcript(video_id, languages=['ru', 'en'])
                return ' '.join([str(item.get('text', '')) for item in data])
            except Exception as e:
                err_msg = str(e)
                if "TranscriptsDisabled" in err_msg:
                    return "[Транскрипты отключены автором]"
                if "NoTranscriptFound" in err_msg:
                    return "[Русские/Английские транскрипты не найдены]"
                # Если бан по IP или другая ошибка - пробуем следующий метод или выводим ошибку
                last_err = err_msg
                continue
    return f"[Ошибка загрузки: {last_err if 'last_err' in locals() else 'Метод не найден'}]"

def parse_video_list(file_path: str) -> List[Dict[str, str]]:
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    
    videos = []
    for i in range(0, len(lines) - 1, 2):
        if 'youtube.com' in lines[i+1] or 'youtu.be' in lines[i+1]:
            videos.append({'title': lines[i], 'url': lines[i+1]})
    return videos

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    video_list_path = os.path.join(base_dir, 'videos_list.txt')
    
    videos = parse_video_list(video_list_path)
    if not videos:
        print(f"Список видео пуст или не найден: {video_list_path}")
        return

    # Берем 20 видео
    target_videos = videos[0:20]
    md_content = "# aiBoomb YouTube Channel Transcripts\n\n"
    
    print(f"Обработка {len(target_videos)} видео...")
    
    for idx, video in enumerate(target_videos, 1):
        url = video['url']
        title = video['title']
        video_id = get_video_id(url)
        
        print(f"[{idx}/{len(target_videos)}] ID: {video_id} | {title}")
        
        if video_id:
            text = fetch_transcript_api(video_id)
        else:
            text = "[Ошибка: Некорректная ссылка]"
        
        md_content += f"## {title}\n**URL:** {url}\n\n{text}\n\n---\n\n"

    out_file = os.path.join(base_dir, "aiBoomb_NotebookLM_Source.md")
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"\nГОТОВО! Файл: {out_file}")

if __name__ == "__main__":
    main()
