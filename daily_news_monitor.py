"""
daily_news_monitor.py
Мониторинг новых видео на aimastodont.com и neuropros.
Запускается раз в день через Windows Task Scheduler.
Новые видео → сохраняются в Obsidian и (опционально) в NotebookLM.
"""
import sys
import os
import json
import hashlib
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path
import re

sys.stdout.reconfigure(encoding='utf-8')

# ── Конфигурация ──────────────────────────────────────────────────────────────
SOURCES = {
    "mastodont": {
        "url": "https://aimastodont.com/",
        "name": "AI Mastodont",
        "emoji": "🤖"
    },
    "neuropros": {
        "url": "https://my.makeunion.me/m/neuropros",
        "name": "Нейропросвещение",
        "emoji": "🧠"
    }
}

OBSIDIAN_DIR = Path(r"C:\ANTIGRAVITY\1\obsidian_brain\0_INBOX")
STATE_FILE   = Path(r"C:\ANTIGRAVITY\1\obsidian_brain\0_INBOX\.news_monitor_state.json")
LOG_FILE     = Path(r"C:\ANTIGRAVITY\1\obsidian_brain\0_INBOX\.news_monitor.log")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# ── Утилиты ───────────────────────────────────────────────────────────────────

def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read().decode("utf-8", errors="replace")


def html_to_lines(html: str) -> list[str]:
    """Грубо извлекаем строки с текстом ссылок/заголовков."""
    # Убираем теги, оставляем текст
    text = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.S)
    text = re.sub(r"<style[^>]*>.*?</style>",  "", text, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"&nbsp;", " ", text)
    text = re.sub(r"&[a-z]+;", "", text)
    lines = [l.strip() for l in text.splitlines() if l.strip() and len(l.strip()) > 10]
    return lines


def fingerprint(lines: list[str]) -> str:
    combined = "\n".join(lines)
    return hashlib.sha256(combined.encode()).hexdigest()


def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {}


def save_state(state: dict):
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    line = f"[{ts}] {msg}"
    print(line)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def extract_new_videos(old_lines: list[str], new_lines: list[str]) -> list[str]:
    """Возвращает строки которые появились в new, но не было в old."""
    old_set = set(old_lines)
    return [l for l in new_lines if l not in old_set and len(l) > 15]


def save_to_obsidian(source_name: str, emoji: str, new_items: list[str]):
    today = datetime.now().strftime("%Y-%m-%d")
    filename = OBSIDIAN_DIR / f"📰 Новости ИИ {today}.md"
    OBSIDIAN_DIR.mkdir(parents=True, exist_ok=True)

    header = f"## {emoji} {source_name} — новое {today}\n\n"
    body = "\n".join(f"- {item}" for item in new_items) + "\n\n"

    if filename.exists():
        existing = filename.read_text(encoding="utf-8")
        # Не дублируем если уже есть этот источник сегодня
        if source_name in existing:
            return
        filename.write_text(existing + header + body, encoding="utf-8")
    else:
        frontmatter = f"---\ntags: [новости, ИИ]\ndate: {today}\n---\n\n"
        filename.write_text(frontmatter + header + body, encoding="utf-8")
    
    log(f"  Obsidian: записано {len(new_items)} новых позиций → {filename.name}")


# ── Главный цикл ──────────────────────────────────────────────────────────────

def main():
    log("=" * 50)
    log("Запуск мониторинга новостей ИИ")
    state = load_state()
    any_new = False

    for key, cfg in SOURCES.items():
        log(f"\n[{cfg['emoji']} {cfg['name']}] Проверка {cfg['url']}")
        try:
            html  = fetch(cfg["url"])
            lines = html_to_lines(html)
            fp    = fingerprint(lines)

            prev = state.get(key, {})
            prev_fp    = prev.get("fingerprint", "")
            prev_lines = prev.get("lines", [])

            if fp == prev_fp:
                log(f"  Без изменений (hash={fp[:12]})")
            else:
                new_items = extract_new_videos(prev_lines, lines)
                log(f"  ИЗМЕНЕНИЕ! Найдено {len(new_items)} новых строк")
                
                if new_items:
                    for item in new_items[:10]:
                        log(f"    + {item[:90]}")
                    save_to_obsidian(cfg["name"], cfg["emoji"], new_items[:20])
                    any_new = True
                else:
                    log(f"  Контент изменился, но новых видео не выявлено (структура)")

            # Обновляем state
            state[key] = {"fingerprint": fp, "lines": lines, "checked": datetime.now().isoformat()}

        except Exception as e:
            log(f"  ОШИБКА: {e}")

    save_state(state)

    if any_new:
        log("\n✅ Есть новые материалы — проверь Obsidian (0_INBOX)")
    else:
        log("\n✅ Всё проверено — новых видео нет")


if __name__ == "__main__":
    main()
