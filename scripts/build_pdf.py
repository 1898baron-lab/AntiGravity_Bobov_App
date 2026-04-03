# build_pdf.py — генератор PDF-гайда «10 hardcore-промптов для инженера-конструктора»
# Используем ReportLab + DejaVu Sans для корректного рендера кириллицы

import os
import urllib.request
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle, PageBreak
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ─── Шрифт DejaVu (кириллица) ─────────────────────────────────────────────────
FONT_DIR = os.path.join(os.path.dirname(__file__), "fonts")
os.makedirs(FONT_DIR, exist_ok=True)

FONTS = {
    "DejaVu":       "https://cdn.jsdelivr.net/npm/dejavu-fonts-ttf@2.37.3/ttf/DejaVuSans.ttf",
    "DejaVu-Bold":  "https://cdn.jsdelivr.net/npm/dejavu-fonts-ttf@2.37.3/ttf/DejaVuSans-Bold.ttf",
    "DejaVu-Italic":"https://cdn.jsdelivr.net/npm/dejavu-fonts-ttf@2.37.3/ttf/DejaVuSans-Oblique.ttf",
}

for name, url in FONTS.items():
    path = os.path.join(FONT_DIR, f"{name}.ttf")
    if not os.path.exists(path):
        print(f"Скачиваю шрифт {name}...")
        urllib.request.urlretrieve(url, path)
    pdfmetrics.registerFont(TTFont(name, path))

# ─── Цветовая палитра ──────────────────────────────────────────────────────────
C_BLUE   = colors.HexColor("#1A3C5E")
C_ACCENT = colors.HexColor("#E8453C")
C_LIGHT  = colors.HexColor("#F0F4F8")
C_GRAY   = colors.HexColor("#6B7280")
C_WHITE  = colors.white

# ─── Стили ────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def S(name, **kw):
    kw.setdefault("fontName", "DejaVu")
    return ParagraphStyle(name, **kw)

sTitle     = S("sTitle",     fontName="DejaVu-Bold", fontSize=26, leading=32, textColor=C_WHITE, alignment=1, spaceAfter=6)
sSubtitle  = S("sSubtitle",  fontName="DejaVu",      fontSize=13, leading=18, textColor=colors.HexColor("#B0C4DE"), alignment=1, spaceAfter=20)
sTagline   = S("sTagline",   fontName="DejaVu-Italic",fontSize=10, textColor=colors.HexColor("#90A4AE"), alignment=1)
sH1        = S("sH1",        fontName="DejaVu-Bold", fontSize=15, leading=20, textColor=C_BLUE, spaceBefore=18, spaceAfter=6)
sH2        = S("sH2",        fontName="DejaVu-Bold", fontSize=12, leading=16, textColor=C_ACCENT, spaceBefore=10, spaceAfter=4)
sBody      = S("sBody",      fontSize=10, leading=15, textColor=colors.HexColor("#2D3748"), spaceAfter=6)
sCode      = S("sCode",      fontSize=9,  leading=13, textColor=colors.HexColor("#1A202C"),
               backColor=colors.HexColor("#EBF4FF"), leftIndent=12, rightIndent=12,
               borderPadding=(6, 10, 6, 10), spaceAfter=8)
sTip       = S("sTip",       fontName="DejaVu-Italic",fontSize=9.5, leading=14, textColor=colors.HexColor("#2F6B35"),
               backColor=colors.HexColor("#F0FFF4"), leftIndent=14, borderPadding=(5, 8, 5, 8), spaceAfter=8)
sFooter    = S("sFooter",    fontSize=8, textColor=C_GRAY, alignment=1)
sNum       = S("sNum",       fontName="DejaVu-Bold", fontSize=38, leading=42, textColor=C_ACCENT, alignment=0)
sTocItem   = S("sTocItem",   fontSize=10, leading=16, textColor=C_BLUE)

# ─── Контент: 10 промптов ─────────────────────────────────────────────────────
PROMPTS = [
    {
        "num": "01",
        "title": "Проверка актуальности ГОСТ / СП",
        "task": "Быстро узнать, действует ли стандарт, не открывая законодательные базы вручную.",
        "prompt": (
            "Ты — нормировщик с 20-летним стажем. Проверь статус документа: [ГОСТ/СП/РД].\n"
            "Укажи: (1) действует / отменён / заменён; (2) если заменён — чем; (3) ключевые изменения\n"
            "по сравнению с предыдущей редакцией (кратко). Если не уверен — скажи прямо."
        ),
        "tools": "ChatGPT-4o / Claude Opus",
        "tip": "Добавь «Сошлись на дату последней редакции» — модель реже галлюцинирует на нормативах.",
    },
    {
        "num": "02",
        "title": "Макрос для КОМПАС-3D / AutoCAD — генерация за 1 минуту",
        "task": "Получить готовый скрипт (Lisp / KLang) без курсов и StackOverflow.",
        "prompt": (
            "Напиши макрос для [КОМПАС-3D v24 / AutoCAD 2022] на [KLang / AutoLisp].\n"
            "Задача: [опиши действие — например: «обойти все чертежи в сборке и заменить штамп\n"
            "организации с «ООО X» на «АО Y»»]. Код снабди комментариями на русском.\n"
            "В конце — инструкция по запуску (2–3 шага)."
        ),
        "tools": "Claude 3.7 Sonnet / GPT-4o",
        "tip": "Вставляй скриншот ошибки компилятора в следующий запрос — модель исправит сама.",
    },
    {
        "num": "03",
        "title": "Расчёт опасной зоны в ППР",
        "task": "Быстро получить расчётное значение и формулу для раздела ППР без ошибок.",
        "prompt": (
            "Выступи как инженер ПТО с опытом разработки ППР для объектов класса КС-3.\n"
            "Рассчитай опасную зону при [операция: монтаж колонны / работа крана / сварка на высоте].\n"
            "Исходные данные: [масса груза, высота подъёма, вылет стрелы и т.д.].\n"
            "Нормативная база: СП 48.13330, ГОСТ 12.3.009, РД 11-06-2007.\n"
            "Формат: (1) формула; (2) подстановка; (3) результат; (4) вывод для ППР одним абзацем."
        ),
        "tools": "GPT-4o / Claude — в режиме «думай вслух»",
        "tip": "Попроси «Проверь размерность всех единиц» — избавит от ошибок перевода кг→т или мм→м.",
    },
    {
        "num": "04",
        "title": "Генерация технических условий (ТУ) на изделие",
        "task": "Черновик ТУ по ГОСТ 2.114 за 10 минут вместо 3 часов.",
        "prompt": (
            "Составь черновик технических условий по ГОСТ 2.114 за изделие: [название], назначение: [описание].\n"
            "Разделы: 1-Технические требования; 2-Требования безопасности; 3-Правила приёмки;\n"
            "4-Методы контроля; 5-Транспортирование и хранение; 6-Гарантии.\n"
            "Применяемые материалы: [список]. Класс точности: [IT]. Среда эксплуатации: [параметры].\n"
            "Используй стиль ЕСКД: безличные обороты, настоящее время, без вводных слов."
        ),
        "tools": "Claude 3.7 (длинный контекст)",
        "tip": "После генерации попроси: «Какие пункты ты не заполнил — перечисли placeholder'ы» — сразу увидишь пробелы.",
    },
    {
        "num": "05",
        "title": "Экспресс-анализ чертежа (загрузи изображение)",
        "task": "Проверить чертёж на типовые ошибки ЕСКД без ручного перечёркивания.",
        "prompt": (
            "На изображении — чертёж детали/сборки. Выполни проверку по ГОСТ 2.109 и ГОСТ 2.307.\n"
            "Найди: (1) ошибки простановки размеров; (2) нарушения оформления штампа;\n"
            "(3) отсутствующие обозначения (шероховатость, допуски, базы); (4) прочее.\n"
            "Выдай результат таблицей: Пункт | Обнаруженная ошибка | Рекомендация."
        ),
        "tools": "GPT-4o Vision / Claude 3.7 (с загрузкой файла)",
        "tip": "Работает лучше с растровым PNG, чем с PDF — конвертируй через FastStone перед загрузкой.",
    },
    {
        "num": "06",
        "title": "Технологическая карта (МК/ОК) по ЕСТД",
        "task": "Черновик операционной или маршрутной карты по ГОСТ 3.1404.",
        "prompt": (
            "Разработай [маршрутную / операционную] карту по ГОСТ 3.1404 для детали: [название].\n"
            "Материал: [марка, ГОСТ]. Переходы: [список операций — токарная, фрезерная, слесарная].\n"
            "Для каждой операции укажи: оборудование; инструмент; режимы (скорость, подача, глубина);\n"
            "разряд; норму времени (ориентировочно). Формат: таблица ЕСТД, безличные обороты."
        ),
        "tools": "GPT-4o / Claude",
        "tip": "После получения таблицы: «Пересчитай Тшт для серии 500 шт с коэффициентом 0.85» — и сразу получишь доработанную норму.",
    },
    {
        "num": "07",
        "title": "Цепочка допусков и посадок — быстрый подбор",
        "task": "Подобрать систему допусков для пары деталей без справочника Мягкова.",
        "prompt": (
            "Подбери посадку для соединения: [описание — вал в корпусе / штифт в отверстии / шпонка].\n"
            "Условия: [нагрузка, характер сборки — подвижное/неподвижное, температурный диапазон].\n"
            "Система [вала / отверстия]. Квалитет: предпочтительно [7-8] класс точности.\n"
            "Результат: (1) рекомендуемая посадка; (2) числовые отклонения (es, ei, ES, EI по ГОСТ 25347);\n"
            "(3) зазор/натяг min/max; (4) обоснование выбора одним предложением."
        ),
        "tools": "GPT-4o",
        "tip": "Запроси «Проверь по таблице предпочтительных посадок ГОСТ 25347-82» — снизит риск выхода за рекомендуемый ряд.",
    },
    {
        "num": "08",
        "title": "Коммерческое предложение / ТЗ для подрядчика — инженерный стиль",
        "task": "Превратить неформальную задачу в структурированный документ для тендера или ТЗ.",
        "prompt": (
            "Ты — ведущий инженер-конструктор. Составь техническое задание / коммерческое предложение\n"
            "на [услуга / изделие]. Исходные данные: [набросок задачи своими словами].\n"
            "Структура: 1-Наименование и объект; 2-Цель; 3-Технические требования; 4-Объём работ;\n"
            "5-Требования к сдаче; 6-Сроки; 7-Ответственность сторон.\n"
            "Стиль: деловой, конкретный, без воды. ГОСТ 34 (если IT-составляющая есть)."
        ),
        "tools": "Claude 3.7 Sonnet",
        "tip": "Добавь «Оцени риски по каждому разделу и выдели их курсивом» — сразу увидишь слабые места ТЗ.",
    },
    {
        "num": "09",
        "title": "Перевод технической документации (EN ↔ RU с сохранением терминологии)",
        "task": "Перевести datasheet, стандарт ISO или инструкцию без потери смысла и терминологии.",
        "prompt": (
            "Переведи следующий технический текст с [EN/DE/FR] на [RU], сохраняя профессиональную терминологию.\n"
            "Область: [машиностроение / сварка / трубопроводы / электроника].\n"
            "Если встречаются аббревиатуры без перевода в русской практике (PLC, CNC, HMI) — оставляй как есть.\n"
            "Термины-кальки не использовать — только устоявшиеся русские эквиваленты.\n"
            "Сноски: если термин спорный — дай варианты в скобках. [ТЕКСТ:]"
        ),
        "tools": "GPT-4o / DeepL API (для массового перевода)",
        "tip": "После перевода: «Проверь перевод на соответствие терминам ГОСТ [номер]» — модель скорректирует под конкретный стандарт.",
    },
    {
        "num": "10",
        "title": "TreeOfThought: системный анализ технической проблемы",
        "task": "Разобрать сложную, нештатную ситуацию структурированно — чтобы не пропустить причину.",
        "prompt": (
            "Применяй метод Tree of Thought (ToT).\n"
            "Проблема: [описание нештатной ситуации — например: «деталь разрушается в зоне сварки после\n"
            "10 000 циклов нагружения при расчётном ресурсе 50 000 циклов»].\n"
            "Шаг 1: Сгенерируй 3–4 гипотезы (ветки дерева).\n"
            "Шаг 2: Для каждой гипотезы — возможные причины (2–3 подпункта) и метод проверки.\n"
            "Шаг 3: Ранжируй ветки по вероятности (высокая/средняя/низкая).\n"
            "Шаг 4: Предложи план верификации (последовательность действий)."
        ),
        "tools": "Claude 3.7 Sonnet / o3",
        "tip": "tree of thought лучше всего работает через o3 или Claude 3.7 extended thinking. Для этого промпта включи «режим расширенного мышления» в настройках.",
    },
]

# ─── Сборка PDF ────────────────────────────────────────────────────────────────
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "pdf_funnel_output")
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "10_prompts_engineer.pdf")

doc = SimpleDocTemplate(
    OUTPUT_FILE,
    pagesize=A4,
    leftMargin=1.8*cm, rightMargin=1.8*cm,
    topMargin=1.5*cm, bottomMargin=1.5*cm,
    title="10 hardcore-промптов для инженера-конструктора",
    author="Бобов Кирилл Олегович × AntiGravity",
)

story = []

# ── Обложка ──
def cover_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(C_BLUE)
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    canvas.setFillColor(C_ACCENT)
    canvas.setLineWidth(0)
    for i in range(0, 600, 48):  # диагональные полосы
        canvas.setFillAlpha(0.04)
        canvas.rect(i, 0, 24, A4[1], fill=1, stroke=0)
    canvas.restoreState()

story.append(Spacer(1, 3.5*cm))
story.append(Paragraph("10 hardcore-промптов", sTitle))
story.append(Paragraph("для инженера-конструктора", sTitle))
story.append(Spacer(1, 0.5*cm))
story.append(Paragraph("ChatGPT &amp; Claude в реальных задачах проектирования", sSubtitle))
story.append(Spacer(1, 0.4*cm))
story.append(HRFlowable(width="60%", thickness=1, color=C_ACCENT, hAlign='CENTER'))
story.append(Spacer(1, 0.4*cm))
story.append(Paragraph("ТУ · ППР · ЕСКД · ЕСТД · Допуски · Макросы САПР · Tree of Thought", sTagline))
story.append(Spacer(1, 1.0*cm))
story.append(Paragraph("AntiGravity × NotebookLM  ·  2026", sFooter))
story.append(PageBreak())

# ── Оглавление ──
story.append(Paragraph("Содержание", sH1))
story.append(HRFlowable(width="100%", thickness=0.5, color=C_BLUE, spaceAfter=8))
for p in PROMPTS:
    story.append(Paragraph(f"<b>Промпт {p['num']}.</b>  {p['title']}", sTocItem))
story.append(PageBreak())

# ── Вступление ──
story.append(Paragraph("Зачем этот гайд?", sH1))
story.append(Paragraph(
    "Каждый из этих промптов — это готовый инструмент, проверенный на реальных задачах: "
    "от разработки ТУ и ТЗ до расчёта опасных зон в ППР и генерации макросов для КОМПАС-3D. "
    "Вставь свои данные (выделены [скобками]) — и получи результат, который раньше занимал часы.",
    sBody
))
story.append(Paragraph(
    "Применяй метки детализации: <b>_1</b> = кратко / <b>_2</b> = развёрнуто / <b>_3</b> = с расчётами и аргументацией.",
    sBody
))
story.append(Spacer(1, 0.4*cm))

# ── Промпты ──
for p in PROMPTS:
    story.append(Paragraph(f"Промпт {p['num']}.", sNum))
    story.append(Paragraph(p["title"], sH1))

    # Задача
    data = [
        [Paragraph("<b>Задача:</b>", sBody), Paragraph(p["task"], sBody)],
        [Paragraph("<b>ИИ:</b>",     sBody), Paragraph(p["tools"], sBody)],
    ]
    t = Table(data, colWidths=[3.2*cm, 12.5*cm])
    t.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("TOPPADDING", (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.25*cm))

    # Промпт
    story.append(Paragraph("<b>📋 Промпт:</b>", sH2))
    for line in p["prompt"].strip().split("\n"):
        story.append(Paragraph(line.strip() or "&nbsp;", sCode))

    # Совет
    story.append(Paragraph(f"💡 <b>Совет:</b>  {p['tip']}", sTip))
    story.append(HRFlowable(width="100%", thickness=0.3, color=colors.HexColor("#CBD5E0"), spaceBefore=10, spaceAfter=10))

# ── Финальный блок ──
story.append(PageBreak())
story.append(Spacer(1, 1.5*cm))
story.append(Paragraph("Что дальше?", sH1))
story.append(Paragraph(
    "Это только старт. Каждый промпт можно превратить в автоматизированный пайплайн:\n"
    "📂 базу знаний компании в NotebookLM → запросы → готовые технические документы.\n"
    "Следующая итерация гайда: промпты для 3D-моделирования, изометрий трубопроводов и ТХК.",
    sBody
))
story.append(Spacer(1, 0.6*cm))
story.append(Paragraph("Эта PDF создана через пайплайн AntiGravity × NotebookLM", sFooter))
story.append(Paragraph("Версия 1.0  ·  2026  ·  Новоуральск", sFooter))

# ── Сборка ──
doc.build(story)
print(f"✅ PDF готов: {OUTPUT_FILE}")
