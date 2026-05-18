---
name: yt_ideas_extractor
description: |
  Автоматически извлекает русскую транскрипцию YouTube‑видео, отбирает ключевые идеи (коррупция, блокировка интернета, контроль, VPN) и сохраняет их в Markdown‑формате. Удобно для пополнения Knowledge Base новыми инсайтами из видеоконтента.
---

# YouTube Ideas Extractor

## Что делает
- Скачивает транскрипцию видео через `youtube_transcript_api`.
- Фильтрует предложения с ключевыми словами (коррупция, блокировка, интернет, власть, VPN, цензура и пр.).
- Формирует файл `*_Summary.md` в папке `1_PROJECTS/Summaries`.

## Как использовать
```bash
$ .venv\Scripts\python.exe c:\ANTIGRAVITY\1\.agents\skills\yt_ideas_extractor\scripts\yt_ideas_extractor.py \
    https://youtu.be/VfoyDMDX9bU?si=7zycaiEFhSz8qMYa \
    <output_path>
```

## Артефакты
- `artifacts/ideas.md` – сырая выжимка (для отладки).
- `.../Summaries/<video_name>_Summary.md` – готовый файл, импортируется в Knowledge Base через `sync_to_brain.py`.

## Интеграция в Knowledge Base
После генерации файл автоматически попадает в `1_PROJECTS/Summaries` и будет синхронизирован скриптом `sync_to_brain.py`.

