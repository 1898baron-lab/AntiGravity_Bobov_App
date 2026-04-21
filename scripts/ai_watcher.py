"""
Mastodont AI Watcher v1.2 — Full-Auto Mode
========================================
Слушает изменения в TO_CHATGPT.md.
Автоматически вызывает AI через Claude Connector.

При изменении файла:
  1. Сканирует Obsidian Engineering/ и находит релевантные документы.
  2. Формирует контекст и отправляет запрос в AI.
  3. Записывает результат в FROM_CHATGPT.md.

Запуск:
  .venv/Scripts/python.exe scripts/ai_watcher.py
"""

import sys
import time
import logging
import json
import httpx
import asyncio
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
MCP_URL   = "http://localhost:8000"          # MCP Bridge
AI_URL    = "http://localhost:8765"          # Claude Connector (API)
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
                    "snippet": content[:5000] # Увеличили для полноты контекста
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


async def call_ai_service(prompt: str, context: str) -> str:
    """Отправляет запрос в Claude Connector."""
    logger.info("🚀 Отправка запроса в AI Service (Claude Connector)...")
    full_prompt = f"System Context (Local Knowledge Base):\n{context}\n\nUser Question:\n{prompt}"
    
    try:
        async with httpx.AsyncClient(timeout=300.0) as client:
            resp = await client.post(
                f"{AI_URL}/v1/messages",
                json={
                    "messages": [{"role": "user", "content": full_prompt}],
                    "model": "claude-3-sonnet-20240229"
                }
            )
            if resp.status_code == 200:
                data = resp.json()
                return data["content"][0]["text"]
            else:
                return f"❌ Ошибка AI Service: {resp.status_code}\n{resp.text}"
    except Exception as e:
        return f"❌ Ошибка подключения к AI Service (localhost:8765): {e}"


def build_final_output(project: str, mode: str, prompt: str, docs: list, ai_response: str) -> str:
    """Формирует финальный Markdown-файл с ответом."""
    ctx_refs = "\n".join([f"- [{d['title']}](file:///{ENG_DIR}/{d['id']})" for d in docs])
    
    return f"""# 📥 Ответ — {project} [{mode}]

*Заполнено автоматически Mastodont Watcher в {time.strftime('%H:%M:%S')}*

---

## 📋 Запрос
{prompt}

---

## 📚 Контекст (База знаний)
{ctx_refs}

---

## ✍️ Ответ AI
{ai_response}

---

**Статус**: Готово. TO_CHATGPT.md готов к новому запросу.
"""


async def main_loop():
    logger.info("=" * 50)
    logger.info("🟢 Mastodont AI Watcher v1.2 запущен (Full-Auto Mode)")
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
                    docs = kb.search(keywords)
                    
                    # Собираем контекст для ИИ
                    context_block = "\n\n".join([f"DOC: {d['title']}\n{d['snippet']}" for d in docs])
                    
                    # Отправляем в ИИ
                    ai_response = await call_ai_service(text, context_block)
                    
                    # Сохраняем результат
                    final_md = build_final_output(
                        meta.get("PROJECT", "General"),
                        meta.get("MODE", "Engineering"),
                        text,
                        docs,
                        ai_response
                    )
                    
                    FROM_FILE.write_text(final_md, encoding="utf-8")
                    logger.info("✅ FROM_CHATGPT.md обновлен ответом от AI.")
                    last_hash = current_hash

        except Exception as e:
            logger.error(f"Ошибка в цикле: {e}")

        await asyncio.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    try:
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        logger.info("👋 Завершение работы Watcher.")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
