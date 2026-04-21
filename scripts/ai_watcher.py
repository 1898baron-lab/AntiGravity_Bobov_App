"""
Mastodont AI Watcher v1.0
===========================
Слушает изменения в TO_CHATGPT.md.
При изменении:
  1. Ищет релевантные документы в локальной базе знаний (через MCP KnowledgeStore).
  2. Формирует "контекстно-обогащённый" запрос.
  3. Записывает его в FROM_CHATGPT.md — готов к отправке в ChatGPT или автоматически через API.

Запуск:
  .venv/Scripts/python.exe scripts/ai_watcher.py
"""

import time
import json
import logging
import httpx
from pathlib import Path

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [WATCHER] %(levelname)s - %(message)s'
)
logger = logging.getLogger("ai_watcher")

# Пути
BASE   = Path(__file__).parent.parent.resolve()
TO_FILE   = BASE / "obsidian_brain/_AI_EXCHANGE/TO_CHATGPT.md"
FROM_FILE = BASE / "obsidian_brain/_AI_EXCHANGE/FROM_CHATGPT.md"
MCP_URL   = "http://localhost:8000"
POLL_INTERVAL = 3  # секунды


def search_local_knowledge(query: str) -> list:
    """Поиск в локальном MCP Bridge."""
    try:
        resp = httpx.post(
            f"{MCP_URL}/messages",
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": "search_knowledge",
                    "arguments": {"query": query}
                }
            },
            timeout=5.0
        )
        if resp.status_code == 200:
            data = resp.json()
            result_text = data.get("result", {}).get("content", [{}])[0].get("text", "{}")
            return json.loads(result_text).get("results", [])
    except Exception as e:
        logger.warning(f"MCP search failed: {e}")
    return []


def extract_query_keywords(text: str) -> str:
    """Простое извлечение ключевых слов из запроса."""
    # Ищем строки типа "## Вопросы" или "query:" или просто берём первые слова
    lines = [l.strip() for l in text.splitlines() if l.strip() and not l.startswith("#")]
    for line in lines:
        if len(line) > 15:
            return line[:80]
    return text[:80]


def build_enriched_output(request_text: str, found_docs: list) -> str:
    """Формирует готовый к использованию ответ с контекстом из базы знаний."""
    context_block = ""
    if found_docs:
        context_block = "## 📚 Контекст из базы знаний (найдено автоматически)\n\n"
        for d in found_docs[:3]:
            context_block += f"### `{d['title']}` (score: {d.get('score', '?')})\n"
            context_block += f"{d.get('snippet', '')}\n\n"
        context_block += "---\n\n"
    else:
        context_block = "> ⚠️ Документы по запросу не найдены в локальной базе.\n\n---\n\n"

    return f"""# 📥 Ответ от ChatGPT

*Заполнено автоматически Mastodont Watcher в {time.strftime('%Y-%m-%d %H:%M:%S')}*

---

## 📋 Оригинальный запрос (из TO_CHATGPT.md)

{request_text[:500]}...

---

{context_block}## ✍️ Ответ ChatGPT

> ***Вставьте сюда ответ от ChatGPT или дождитесь API-версии***

---
*Дайджест основных тезисов:*
- ...
- ...
- ...
"""


def run():
    logger.info("🟢 Mastodont AI Watcher запущен.")
    logger.info(f"  Слушаю: {TO_FILE}")
    logger.info(f"  Вывод:  {FROM_FILE}")
    logger.info(f"  MCP:    {MCP_URL}")
    logger.info(f"  Интервал: {POLL_INTERVAL} сек.\n")

    last_hash = ""

    while True:
        try:
            if TO_FILE.exists():
                text = TO_FILE.read_text(encoding="utf-8")
                current_hash = str(hash(text))

                if text.strip() and current_hash != last_hash:
                    logger.info("🔔 Изменение обнаружено в TO_CHATGPT.md")

                    # Извлекаем ключевые слова для поиска
                    keywords = extract_query_keywords(text)
                    logger.info(f"🔍 Поиск по ключевым словам: '{keywords}'")

                    # Ищем в локальной базе знаний
                    found = search_local_knowledge(keywords)
                    logger.info(f"📚 Найдено документов: {len(found)}")

                    # Формируем выходной файл
                    output = build_enriched_output(text, found)
                    FROM_FILE.write_text(output, encoding="utf-8")

                    logger.info(f"✅ FROM_CHATGPT.md обновлен. Вставьте ответ ChatGPT в файл.")
                    last_hash = current_hash
            else:
                logger.warning(f"TO_CHATGPT.md не найден: {TO_FILE}")

        except Exception as e:
            logger.error(f"Ошибка в цикле: {e}")

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    run()
