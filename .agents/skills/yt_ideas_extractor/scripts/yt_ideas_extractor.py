"""
YT Ideas Extractor
Извлекает русскую транскрипцию YouTube‑видео и формирует
короткую выжимку с идеями/тезисами.
"""

import sys
from pathlib import Path
from youtube_transcript_api import YouTubeTranscriptApi


def fetch_transcript(video_id: str) -> str:
    """Получить русскую транскрипцию, fallback‑англ."""
    try:
        # In the installed version, YouTubeTranscriptApi().list() is available
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)
        try:
            transcript = transcript_list.find_transcript(['ru']).fetch()
        except:
            # Fallback to English
            transcript = transcript_list.find_transcript(['en']).fetch()
            
        # Depending on version, snippet is either a dict or FetchedTranscriptSnippet object
        return " ".join([t['text'] if isinstance(t, dict) else t.text for t in transcript])
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return ""


import httpx
import json

def extract_ideas(text: str) -> str:
    """Используем локальный LLM для выделения главных идей и формирования выжимки."""
    url = "http://127.0.0.1:1234/v1/chat/completions"
    
    prompt = f"""
Проанализируй следующий транскрипт видео. 
Выдели главные тезисы, инсайты и ключевые идеи. 
Оформи ответ в виде структурированной Markdown-статьи с заголовками и списками.
Переведи на русский язык, если необходимо.

Транскрипт:
{text[:5000]}  # Ограничиваем длину во избежание переполнения контекста (max_ctx 2560)
"""
    
    payload = {
        "model": "google/gemma-4-e4b",
        "messages": [
            {"role": "system", "content": "Ты — профессиональный аналитик и эксперт по структурированию информации. Твоя цель — вытаскивать самую суть из текстов."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 2048
    }
    
    try:
        with httpx.Client(timeout=120.0) as client:
            response = client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
    except httpx.HTTPStatusError as e:
        print(f"Ошибка HTTP: {e.response.status_code}")
        print(f"Детали: {e.response.text}")
        return "Не удалось сформировать выжимку с помощью ИИ (Ошибка 400)."
    except Exception as e:
        print(f"Ошибка обращения к локальному ИИ: {e}")
        return "Не удалось сформировать выжимку с помощью ИИ."


def main(video_url: str, out_path: Path):
    if "youtu.be" in video_url:
        video_id = video_url.split('/')[-1].split('?')[0]
    else:
        video_id = video_url.split('v=')[-1].split('&')[0]
    
    raw = fetch_transcript(video_id)
    ideas_md = extract_ideas(raw)
    header = f"# Идеи из видео «{video_url}»\n\n"
    out_path.write_text(header + ideas_md, encoding="utf-8")
    print(f"[DONE] Выжимка записана в {out_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: yt_ideas_extractor.py <video_url> <output_md>")
        sys.exit(1)
    main(sys.argv[1], Path(sys.argv[2]))
