# 📊 MASTADONT System Dashboard

Добро пожаловать в центр управления **MASTADONT AI Factory**. Это живой документ, отражающий статус вашей ИИ-инфраструктуры.

---

## 🚦 Статус систем

| Инструмент | Статус | Адрес / Ресурс |
|------------|--------|----------------|
| **Claude Connector** | 🟢 ACTIVE | `http://localhost:8765` |
| **Gemma + Ollama** | 🔧 READY | `http://localhost:11434` |
| **NotebookLM MCP** | 🟢 READY | [Control Panel](https://notebooklm.google.com) |
| **Obsidian Brain** | 🟢 ACTIVE | `C:\ANTIGRAVITY\1\obsidian_brain` |
| **ChatGPT Bridge** | 🟢 ONLINE | [Refined RAG Server](file:///c:/ANTIGRAVITY/1/scripts/mcp_chatgpt_bridge.py) |
| **Git Sync** | 🟢 SYNCED | [GitHub Repo](https://github.com/1898baron-lab/AntiGravity_Bobov_App) |
| **Internship DB** | 🟢 ACTIVE | [Internship Dashboard](file:///C:/Users/Sasha  Baron/.gemini/antigravity/brain/2ccb1232-8075-4c17-bcc3-8bdc7c1b44fa/internship_training_dashboard.md) |

---

## 🧠 Активные AI-Скиллы (Skills)

Эти скиллы можно вызывать через `/` в чате с агентом:

1.  **[3D Web Builder](file:///C:/ANTIGRAVITY/1/.agents/skills/3d_web_builder.md)**: Генерация премиальных сайтов (Видео #13).
2.  **[SEO Optimizer](file:///C:/ANTIGRAVITY/1/.agents/skills/seo_optimizer.md)**: Полный аудит и доработка SEO.
3.  **[Mastadont Advisor](file:///C:/ANTIGRAVITY/1/.agents/skills/mastadont_advisor/SKILL.md)**: Стратегия монетизации.

---

## ⚡ Быстрый запуск

```bash
# Запуск Claude Connector
python scripts/claude_connector/claude_connector.py

# Запуск Gemma + Ollama теста
python scripts/gemma_ollama.py status

# Запуск локального Ollama-прокси
python scripts/ollama_connector.py --port 11435

# Настройка для AI proxy
export AI_URL="http://localhost:11435"
export AI_ENDPOINT="/api/generate"
export AI_MODEL="gemma-4-e2b-it"

# Запуск Telegram-бота
python pdf_funnel_output/telegram_bot.py
```

---

## 📁 Полезные ссылки
- [README по интеграции Claude](file:///C:/ANTIGRAVITY/1/Инструкция_по_интеграции_Claude_и_Notebook_LM.pdf)
- [Транскрипты Мастадонта](file:///C:/ANTIGRAVITY/1/mastadont_videos_transcript.txt)

> [!TIP]
> Всегда проверяйте, запущен ли **Claude Connector** перед началом работы со скиллами 3D-дизайна.
