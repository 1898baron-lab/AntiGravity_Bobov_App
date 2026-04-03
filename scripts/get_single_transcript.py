from youtube_transcript_api import YouTubeTranscriptApi
import importlib.metadata

VIDEO_ID = "vXx8RE0sxXE"
OUTPUT_FILE = r"C:\ANTIGRAVITY\1\skills_video_transcript.md"

ver = importlib.metadata.version("youtube-transcript-api")
print(f"youtube-transcript-api v{ver}")
print(f"Получаю транскрипт для: {VIDEO_ID}")

text = ""

# Попытка 1: новый API v1.x (экземпляр + fetch)
try:
    api = YouTubeTranscriptApi()
    fetched = api.fetch(VIDEO_ID, languages=['ru'])
    # Объект итерабельный — каждый элемент это snippet
    text = ' '.join([s.text if hasattr(s, 'text') else str(s) for s in fetched])
    print(f"✅ Метод 1 (v1.x instance). Символов: {len(text)}")
except Exception as e1:
    print(f"Метод 1 ошибка: {e1}")
    # Попытка 2: старый API (статический метод)
    try:
        result = YouTubeTranscriptApi.get_transcript(VIDEO_ID, languages=['ru'])
        text = ' '.join([s['text'] for s in result])
        print(f"✅ Метод 2 (static). Символов: {len(text)}")
    except Exception as e2:
        print(f"Метод 2 ошибка: {e2}")
        # Попытка 3: без указания языка
        try:
            api = YouTubeTranscriptApi()
            fetched = api.fetch(VIDEO_ID)
            text = ' '.join([s.text if hasattr(s, 'text') else s.get('text','') for s in fetched])
            print(f"✅ Метод 3 (без языка). Символов: {len(text)}")
        except Exception as e3:
            print(f"Все методы не сработали: {e3}")
            exit(1)

if not text:
    print("Транскрипт пуст!")
    exit(1)

content = (
    "## NotebookLM Получил НОВУЮ Суперсилу (AntiGravity)\n"
    f"**URL:** https://www.youtube.com/watch?v={VIDEO_ID}\n\n"
    f"{text}\n"
)

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ Файл сохранён: {OUTPUT_FILE}")
print(f"\nПервые 500 символов:\n{text[:500]}")
