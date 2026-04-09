# 📊 MASTADONT System Dashboard

Добро пожаловать в центр управления **MASTADONT AI Factory**. Это живой документ, отражающий статус вашей ИИ-инфраструктуры.

---

## 🚦 Статус систем

| Инструмент | Статус | Адрес / Ресурс |
|------------|--------|----------------|
| **Claude Connector** | 🟢 ACTIVE | `http://localhost:8765` |
| **NotebookLM MCP** | 🟢 READY | [Control Panel](https://notebooklm.google.com) |
| **Telegram Bot** | 🟡 STANDBY | `pdf_funnel_output/telegram_bot.py` |
| **Git Sync** | 🟢 SYNCED | [GitHub Repo](https://github.com/1898baron-lab/AntiGravity_Bobov_App) |

---

## 🧠 Активные AI-Скиллы (Skills)

Эти скиллы можно вызывать через `/` в чате с агентом:

1.  **[3D Web Builder](file:///C:/ANTIGRAVITY/1/.agents/skills/3d_web_builder.md)**: Генерация премиальных сайтов (Видео #13).
2.  **[SEO Optimizer](file:///C:/ANTIGRAVITY/1/.agents/skills/seo_optimizer.md)**: Полный аудит и доработка SEO.
3.  **[Mastadont Advisor](file:///C:/ANTIGRAVITY/1/.agents/skills/mastadont_advisor/SKILL.md)**: Стратегия монетизации.

---

## ⚡ Быстрый запуск

```powershell
# Запуск Claude Connector
& "C:\ANTIGRAVITY\1\.venv\Scripts\python.exe" scripts/claude_connector/claude_connector.py

# Запуск Telegram-бота
& "C:\ANTIGRAVITY\1\.venv\Scripts\python.exe" pdf_funnel_output/telegram_bot.py
```

---

## 📁 Полезные ссылки
- [README по интеграции Claude](file:///C:/ANTIGRAVITY/1/Инструкция_по_интеграции_Claude_и_Notebook_LM.pdf)
- [Транскрипты Мастадонта](file:///C:/ANTIGRAVITY/1/mastadont_videos_transcript.txt)

> [!TIP]
> Всегда проверяйте, запущен ли **Claude Connector** перед началом работы со скиллами 3D-дизайна.
