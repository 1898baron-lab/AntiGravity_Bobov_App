"""
telegram_bot.py — Корпоративный ИИ-ассистент РОСАТОМ × AntiGravity

Логика:
1. /start → приветствие с описанием функций.
2. Текст → ИИ-обработка (пока заглушка).
3. Документ → сохранение в локальную базу знаний (legal).

Установка:
    pip install aiogram

Запуск:
    python telegram_bot.py
"""

import sys
print(f"[DEBUG] Запуск бота {__file__}...", flush=True)

import asyncio
import os
import aiohttp
import json
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
import subprocess
from aiogram.types import FSInputFile, InlineKeyboardButton
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

# ── Конфигурация ──────────────────────────────────────────────────────────────
# Явный поиск .env в корне проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ── Тексты ────────────────────────────────────────────────────────────────────
MSG_START = (
    "Привет! 👋\n\n"
    "Я цифровой ассистент <b>Borisco AI FACTORY</b>.\n\n"
    "Я работаю в режиме <b>непрерывного диалога</b> — я помню всё, что мы обсуждали ранее.\n\n"
    "📁 <b>База знаний</b>: отправь мне документ, и я сохраню его в папку <code>legal</code>.\n"
    "🧠 <b>Аналитика</b>: просто пиши мне вопросы.\n"
    "🆕 <b>Сброс</b>: команда /new начнёт новый чат."
)

# Хранилище сессий (в памяти для простоты, можно заменить на JSON)
USER_SESSIONS = {}

# ── Инициализация ─────────────────────────────────────────────────────────────
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp  = Dispatcher()

# ── Хэндлеры ─────────────────────────────────────────────────────────────────
@dp.message(CommandStart())
async def handle_start(message: types.Message):
    """Команда /start → приветствие."""
    await message.answer(MSG_START)

@dp.message(F.text == "/new")
async def handle_new_chat(message: types.Message):
    """Сброс контекста."""
    user_id = message.from_user.id
    if user_id in USER_SESSIONS:
        del USER_SESSIONS[user_id]
    await message.answer("✅ Контекст сброшен! Начинаю новый диалог.")

@dp.message(F.document)
async def handle_document(message: types.Message):
    """Файловый Менеджер: Сохранение документов в папку legal для базы знаний."""
    file_id = message.document.file_id
    file_name = message.document.file_name
    
    # Путь к папке legal (выходим из pdf_funnel_output на уровень выше)
    save_dir = os.path.join(os.path.dirname(__file__), "..", "legal")
    os.makedirs(save_dir, exist_ok=True)
    destination = os.path.join(save_dir, file_name)
    
    file = await bot.get_file(file_id)
    await bot.download_file(file.file_path, destination)
    
    # 🐙 GitHub Auto-Sync (Skill #1)
    try:
        # Путь к корню проекта (на уровень выше от скрипта бота)
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        
        # Выполнение цепочки команд Git через subprocess
        subprocess.run(["git", "add", destination], cwd=project_root, check=True)
        commit_msg = f"docs: добавлен файл {file_name} через SuperBot (Telegram)"
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=project_root, check=True)
        subprocess.run(["git", "push"], cwd=project_root, check=True)
        
        # Формирование ссылки на файл в GitHub
        repo_file_url = f"https://github.com/1898baron-lab/AntiGravity_Bobov_App/blob/main/legal/{file_name}"
        
        await message.answer(
            f"✅ Документ <b>{file_name}</b> сохранён и синхронизирован с GitHub!\n"
            f"🔗 <a href='{repo_file_url}'>Просмотреть в репозитории</a>"
        )
    except Exception as e:
        await message.answer(
            f"✅ Документ сохранён локально, но GitHub-синхронизация не удалась:\n"
            f"<code>{str(e)}</code>"
        )

# ── ИИ-Интеграция ─────────────────────────────────────────────────────────────
CLAUDE_URL = "http://localhost:8765/v1/messages"

async def ask_claude(prompt: str, chat_url: str | None = None):
    """Вызов локального Claude Connector через MCP с поддержкой URL чата."""
    payload = {
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 1024,
        "messages": [{"role": "user", "content": prompt}],
        "metadata": {"chat_url": chat_url}
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(CLAUDE_URL, json=payload, timeout=90) as response:
                if response.status == 200:
                    data = await response.json()
                    # Возвращаем текст и новый URL чата
                    return data["content"][0]["text"], data.get("id")
                else:
                    err_text = await response.text()
                    return f"❌ Ошибка Claude (Status: {response.status}): {err_text}", None
    except Exception as e:
        return f"❌ Ошибка подключения к Claude Connector: {str(e)}", None

@dp.message(F.text & ~F.text.startswith('/'))
async def handle_text_query(message: types.Message):
    """ИИ-Консультант: Обработка текстовых запросов через Claude с памятью и полной базой знаний."""
    user_id = message.from_user.id
    user_text = message.text
    
    # 1. Загружаем юридический контекст (Скилл)
    skill_path = os.path.join(BASE_DIR, ".agents", "skills", "legal_expert_bobov", "SKILL.md")
    # 2. Загружаем свежий бриф (Артефакт)
    # Используем абсолютный путь для Windows
    brief_path = r"C:\Users\Sasha  Baron\.gemini\antigravity\brain\8f3b4cf8-6d07-4a34-8882-82e5ba8c2d21\legal_attack_brief.md"
    
    context_data = ""
    try:
        if os.path.exists(skill_path):
            with open(skill_path, 'r', encoding='utf-8') as f:
                context_data += f"SKILL DATA:\n{f.read()}\n\n"
        if os.path.exists(brief_path):
            with open(brief_path, 'r', encoding='utf-8') as f:
                context_data += f"ACTUAL CASE BRIEF:\n{f.read()}\n\n"
    except Exception as e:
        context_data = f"Ошибка загрузки контекста: {str(e)}"

    # Формируем расширенный промпт (Системная установка)
    system_priming = (
        "Ты — Бориско ИИ, экспертный юридический адвокат по делу Бобова Олега.\n"
        "Твоя задача: использовать предоставленные данные для защиты интересов Олега.\n"
        "Используй агрессивную тактику: 'Имущество на 12 млн — это не мусор'.\n\n"
        f"{context_data}\n"
    )
    
    full_prompt = f"{system_priming}ЗАПРОС ПОЛЬЗОВАТЕЛЯ: {user_text}"
    
    # Получаем URL текущего чата для этого пользователя
    current_chat_url = USER_SESSIONS.get(user_id)
    
    # Визуальный индикатор "печатает"
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    
    # Вызов ИИ
    response_text, new_chat_url = await ask_claude(full_prompt, chat_url=current_chat_url)
    
    # Сохраняем URL чата для следующего раза (Memory)
    if new_chat_url:
        USER_SESSIONS[user_id] = new_chat_url
    
    # Формируем ответ
    if response_text.startswith(("❌", "Ошибка:")):
        full_response = f"⚠️ <b>Проблема с ИИ-движком:</b>\n\n{response_text}"
    else:
        full_response = f"🧠 <b>Borisco AI Advocate:</b>\n\n{response_text}"
    
    await message.answer(full_response)

# ── Запуск ────────────────────────────────────────────────────────────────────

async def main():
    print("[Bot] Бот запущен. Ctrl+C для остановки.")
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
