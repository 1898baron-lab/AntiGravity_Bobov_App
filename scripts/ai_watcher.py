"""
Mastodont AI Watcher v1.1 — Direct Mode
========================================
Слушает изменения в TO_CHATGPT.md.
Напрямую использует KnowledgeStore (без HTTP-запросов).

При изменении файла:
  1. Сканирует Obsidian Engineering/ и находит релевантные документы.
  2. Формирует обогащённый контекст в FROM_CHATGPT.md.
  3. FROM_CHATGPT.md = готовый файл для вставки в ChatGPT или API-запрос.

Запуск:
  .venv/Scripts/python.exe scripts/ai_watcher.py
"""

import sys
import time
import logging
from pathlib import Path

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [WATCHER] %(levelname)s - %(message)s'
)
logger = logging.getLogger("ai_watcher")

# Добавляем scripts/ в пути для импорта KnowledgeStore
BASE = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(BASE / "scripts"))

# Пути
TO_FILE   = BASE / "obsidian_brain/_AI_EXCHANGE/TO_CHATGPT.md"
FROM_FILE = BASE / "obsidian_brain/_AI_EXCHANGE/FROM_CHATGPT.md"
ENG_DIR   = BASE / "obsidian_brain/Engineering"
POLL_INTERVAL = 3  # секунды


class LocalKnowledge:
    """Минимальный локальный поиск по Obsidian без HTTP."""
    def __init__(self, path: Path):
        self.path = path
        self.cache: dict = {}
        self._load()

    def _load(self):
        logger.info(f"Indexing: {self.path}")
        count = 0
        for f in self.path.rglob("*.md"):
            try:
                self.cache[str(f.relative_to(self.path))] = f.read_text(encoding="utf-8")
                count += 1
            except Exception as e:
                logger.warning(f"Skip {f}: {e}")
        logger.info(f"Indexed {count} documents.")

    def search(self, query: str, top_n: int = 3) -> list:
        if not query.strip():
            return []
        q = query.lower()
        results = []
        for doc_id, content in self.cache.items():
            c = content.lower()
            if q in c or q in doc_id.lower():
                score = c.count(q) + (10 if q in doc_id.lower() else 0)
                results.append({
                    "id": doc_id,
                    "title": Path(doc_id).name,
                    "score": score,
                    "snippet": content[:400].replace("\n", " ")
                })
        return sorted(results, key=lambda x: x["score"], reverse=True)[:top_n]


def extract_mode_and_keywords(text: str) -> tuple:
    """Извлекает MODE/PROJECT/TASK_TYPE и ключевые слова для поиска."""
    meta = {}
    for line in text.splitlines():
        for key in ["MODE", "PROJECT", "TASK_TYPE"]:
            if line.strip().startswith(f"## {key}:"):
                meta[key] = line.split(":", 1)[1].strip()

    # Ключевые слова: из PROJECT или первая значимая строка
    keywords = meta.get("PROJECT", "")
    if not keywords:
        for line in text.splitlines():
            line = line.strip()
            if line and not line.startswith("#") and not line.startswith("*") and len(line) > 15:
                keywords = line[:80]
                break
    return meta, keywords


def build_output(text: str, docs: list, meta: dict) -> str:
    mode    = meta.get("MODE", "GENERAL")
    project = meta.get("PROJECT", "Unknown")
    task    = meta.get("TASK_TYPE", "Unknown")

    ctx = ""
    if docs:
        ctx = "## 📚 Релевантные документы из базы знаний\n\n"
        for d in docs:
            ctx += f"### `{d['title']}` _(score: {d['score']})_\n"
            ctx += f"{d['snippet']}...\n\n"
    else:
        ctx = "> ⚠️ Документы по ключевым словам не найдены. Проверьте базу знаний.\n\n"

    preview = "\n".join(text.strip().splitlines()[:20])  # первые 20 строк запроса

    return f"""# 📥 Ответ — {project} [{mode}]

*Обновлено Mastodont Watcher: {time.strftime('%Y-%m-%d %H:%M:%S')}*
*TASK_TYPE: {task}*

---

## 📋 Запрос (превью)

```
{preview}
```

---

{ctx}---

## ✍️ Ответ ChatGPT

<!-- Вставьте сюда ответ от ChatGPT. Watcher не тронет файл, пока TO_CHATGPT.md не изменится. -->


---

**Тезисы:**
- ...
- ...
- ...
"""


def run():
    logger.info("=" * 50)
    logger.info("🟢 Mastodont AI Watcher v1.1 запущен (Direct Mode)")
    logger.info(f"   TO:    {TO_FILE}")
    logger.info(f"   FROM:  {FROM_FILE}")
    logger.info(f"   База:  {ENG_DIR}")
    logger.info("=" * 50)

    kb = LocalKnowledge(ENG_DIR)
    last_hash = ""

    while True:
        try:
            if TO_FILE.exists():
                text = TO_FILE.read_text(encoding="utf-8")
                current_hash = str(hash(text))

                if text.strip() and current_hash != last_hash:
                    logger.info("🔔 Изменение обнаружено в TO_CHATGPT.md")

                    meta, keywords = extract_mode_and_keywords(text)
                    logger.info(f"   MODE={meta.get('MODE')} | PROJECT={meta.get('PROJECT')} | TASK={meta.get('TASK_TYPE')}")
                    logger.info(f"🔍 Поиск: '{keywords}'")

                    docs = kb.search(keywords)
                    logger.info(f"📚 Найдено: {len(docs)} документов")
                    for d in docs:
                        logger.info(f"   └─ [{d['score']:>3}] {d['title']}")

                    output = build_output(text, docs, meta)
                    FROM_FILE.write_text(output, encoding="utf-8")

                    logger.info("✅ FROM_CHATGPT.md обновлен.")
                    last_hash = current_hash

        except Exception as e:
            logger.error(f"Ошибка: {e}")

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    run()
