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

import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import FSInputFile, InlineKeyboardButton
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

# ── Конфигурация ──────────────────────────────────────────────────────────────
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ── Тексты ────────────────────────────────────────────────────────────────────
MSG_START = (
    "Привет! 👋\n\n"
    "Я цифровой ассистент РОСАТОМ × AntiGravity.\n\n"
    "Зачем я существую:\n"
    "📁 <b>База знаний</b>: отправь мне любой документ в чат, и я автоматически сохраню его в корпоративный репозиторий.\n"
    "🧠 <b>Аналитика текста</b>: напиши мне любой вопрос, и мой ИИ-движок обработает его."
)

# ── Инициализация ─────────────────────────────────────────────────────────────
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp  = Dispatcher()

# ── Хэндлеры ─────────────────────────────────────────────────────────────────
@dp.message(CommandStart())
async def handle_start(message: types.Message):
    """Команда /start → приветствие."""
    await message.answer(MSG_START)

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
    
    await message.answer(f"✅ Документ <b>{file_name}</b> сохранён в базу (папка <code>legal</code>).\nПозже я смогу его анализировать и синхронизировать с GitHub!")

@dp.message(F.text & ~F.text.startswith('/'))
async def handle_text_query(message: types.Message):
    """ИИ-Консультант (Заглушка): Обработка текстовых запросов к базе знаний."""
    user_text = message.text
    # Здесь позже будет вызов API (OpenAI/Claude)
    await message.answer("🧠 <b>ИИ-движок в режиме ожидания (ожидается API-ключ).</b>\nТы написал: " + user_text[:50] + ("..." if len(user_text) > 50 else ""))

# ── Запуск ────────────────────────────────────────────────────────────────────

async def main():
    print("[Bot] Бот запущен. Ctrl+C для остановки.")
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
