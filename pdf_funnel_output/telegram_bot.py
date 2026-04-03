"""
telegram_bot.py — PDF-воронка «10 промптов для инженера»

Логика:
1. Любое сообщение → кнопка «Получить PDF 📄»
2. Пользователь нажимает кнопку → бот отправляет PDF
3. После отправки → предложение подписаться на канал (настраивается)

Установка:
    pip install aiogram

Запуск:
    python telegram_bot.py

Переменные (задай здесь или через переменные окружения):
"""

import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import FSInputFile, InlineKeyboardButton

# ── Конфигурация ──────────────────────────────────────────────────────────────
BOT_TOKEN   = os.getenv("BOT_TOKEN", "ВАШ_ТОКЕН_ЗДЕСЬ")      # @BotFather
CHANNEL_URL = os.getenv("CHANNEL_URL", "https://t.me/ВАШ_КАНАЛ")  # для «подписаться»
PDF_PATH    = os.path.join(os.path.dirname(__file__), "pdf_funnel_output", "10_prompts_engineer.pdf")

# ── Тексты ────────────────────────────────────────────────────────────────────
MSG_START = (
    "Привет! 👋\n\n"
    "Я выдаю бесплатный PDF-гайд:\n\n"
    "📘 <b>«10 hardcore-промптов для инженера-конструктора»</b>\n\n"
    "Внутри:\n"
    "✅ Проверка ГОСТов за 30 секунд\n"
    "✅ Генерация макросов для КОМПАС-3D / AutoCAD\n"
    "✅ Расчёт опасных зон в ППР\n"
    "✅ Черновик ТУ и техкарт по ЕСКД/ЕСТД\n"
    "✅ Метод Tree of Thought для сложных задач\n\n"
    "Нажми кнопку 👇 — и PDF придёт прямо в этот чат."
)

MSG_AFTER_PDF = (
    "🎉 Готово! PDF у тебя.\n\n"
    "Там 10 готовых промптов с примерами подстановки данных.\n\n"
    "💡 Если полезно — подпишись на канал, там будут новые инструменты для инженеров:"
)

MSG_ALREADY_SENT = (
    "📄 Уже отправил тебе PDF выше.\n"
    "Если потерял — нажми кнопку ещё раз, пришлю заново."
)

# ── Инициализация ─────────────────────────────────────────────────────────────
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp  = Dispatcher()

# Храним tg_id пользователей, которые уже получили PDF (в памяти, для простоты)
sent_to: set[int] = set()

# ── Кнопки ────────────────────────────────────────────────────────────────────
def kb_get_pdf():
    builder = InlineKeyboardBuilder()
    builder.button(text="📄 Получить PDF", callback_data="get_pdf")
    return builder.as_markup()

def kb_subscribe():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="📢 Подписаться на канал", url=CHANNEL_URL),
        InlineKeyboardButton(text="📥 Получить PDF ещё раз", callback_data="get_pdf"),
    )
    return builder.as_markup()

# ── Хэндлеры ─────────────────────────────────────────────────────────────────
@dp.message(CommandStart())
@dp.message(F.text)
async def handle_start(message: types.Message):
    """Любое сообщение или /start → приветствие с кнопкой."""
    await message.answer(MSG_START, reply_markup=kb_get_pdf())


@dp.callback_query(F.data == "get_pdf")
async def send_pdf(callback: types.CallbackQuery):
    """Кнопка «Получить PDF» → отправляем файл."""
    uid = callback.from_user.id
    await callback.answer()  # убираем «часики» на кнопке

    try:
        pdf_file = FSInputFile(PDF_PATH, filename="10_prompts_engineer.pdf")
        await callback.message.answer_document(
            pdf_file,
            caption=(
                "📘 <b>10 hardcore-промптов для инженера-конструктора</b>\n"
                "ChatGPT &amp; Claude в реальных задачах проектирования\n\n"
                "<i>Версия 1.0 · 2026 · AntiGravity × NotebookLM</i>"
            )
        )
        sent_to.add(uid)
        await callback.message.answer(MSG_AFTER_PDF, reply_markup=kb_subscribe())
    except FileNotFoundError:
        await callback.message.answer(
            "⚠️ PDF временно недоступен. Напиши нам — пришлём вручную."
        )

# ── Запуск ────────────────────────────────────────────────────────────────────
async def main():
    print("🤖 Бот запущен. Ctrl+C для остановки.")
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
