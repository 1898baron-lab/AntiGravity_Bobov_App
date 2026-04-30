# MASTODONT AI SKILLS 2026: Consolidation & Grounding

> [!IMPORTANT]
> Это основной документ методологии "Мастодонт". Все действия ИИ-агента должны соответствовать этим принципам. Приоритет: Скорость, Визуальное Качество, Автономия.

---

## 🛠 Ключевой Стек (Mastodont Stack 2026)

1. **Core Agent:** [Claude Code](https://claude.ai/code) (через OpenRouter).
   - **Endpoint:** `ANTHROPIC_BASE_URL=https://openrouter.ai/api`
   - **Model:** `anthropic/claude-3.5-sonnet:beta`
2. **Data Recon:** [FireCrawl](https://firecrawl.dev)
   - Используется для извлечения брендинга (`scrape`), структуры сайта и семантического анализа конкурентов.
3. **Visual Engine:** [Nano Banana 2](https://deepmind.google/technologies/imagen-3/) (Imagen 3 / Google)
   - Генерация 3D-ассетов, "взрывных" схем продуктов и текстур премиум-класса.
4. **UI/UX Builder:** [Google Stitch](https://stitch.google.com)
   - Дизайн-агент для сборки многостраничных React-приложений в режиме 3X (3 варианта одновременно).

---

## 🚀 Алгоритм "Бизнес за Один Вечер" (Vibe Coding Flow)

### Шаг 1: Разведка (FireCrawl)
- **Задача:** Получить ДНК бренда.
- **Инструкция:** Используй `scrape` URL конкурента. Извлеки `Branding Images`, шрифты и основные смыслы.
- **Цель:** Понять "Vibe" лидера рынка и сделать лучше.

### Шаг 2: Визуальные Инъекции (Nano Banana 2)
- **Техника:** "Explosion Shot".
- **Промпт:** `3D deconstructed version of [product], floating parts, ultra-detailed 8k, soft lighting, isolated on white background`.
- **Зачем:** Создает ощущение "дорогого Apple-style" продукта.

### Шаг 3: Сборка в Stitch
- **Метод:** Перенос URL референса в Stitch.
- **Prompting:** "Создай трехстраничное приложение в стиле [Reference URL], сохранив шрифты, но улучшив UX".
- **Export:** Выгрузка в ZIP или напрямую в AntiGravity (VS Code).

### Шаг 4: Адаптация и Деплой (Claude Code + Vercel)
- **Задача:** Оживить дизайн.
- **Команда:** "Клод, возьми ZIP из Stitch, почисти код, добавь скролл-анимацию 3D-модели (parallax) и запушь на GitHub".
- **Deploy:** Связка `GitHub -> Vercel` для мгновенной публикации.

---

## 🔒 Инфраструктура и Безопасность (Grounded Instructions)

### Настройка Среды
- **VPS:** Рекомендуется использование выделенных серверов (NetEase/аналоги) для обхода региональных ограничений.
- **VPN:** Использование строго корпоративных или выделенных IP для работы с API Claude и NotebookLM.
- **Identity:** Никаких логов в публичных репозиториях. Использовать `.env.example`.

### Безопасность данных
- При работе с юридическими кейсами (Проект "Зевс") — использовать паттерн **"Zero Knowledge"**: не передавать персональные данные (ФИО, номера дел) в открытых промптах, заменяя их на плейсхолдеры.

---

## 🧠 Система Памяти (Infinite Memory Pattern)

1. **Enrichment**: Каждая новая задача в Claude Code начинается с анализа `knowledge` папки.
2. **Multiplication**: После выполнения задачи — генерация контента (пост, отчет, документация) для фиксации успеха.
3. **Wrapup**: Обновление текущего файла `mastodont_skills.md` новыми найденными "хаками".

---

## 💸 Монетизация (Mastodont Funnels)
- **Lead Magnet:** Бесплатный аудит сайта через AI-агента.
- **Main Product:** Автоматизация B2B отделов продаж (AI-звонари + CRM-интеграции).
- **Strategy:** "Не будь исполнителем — будь Архитектором Смыслов".

---
*Created by Antigravity Model via Mastodont Methodology. 2026.*
