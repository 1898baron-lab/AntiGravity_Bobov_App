---
tags:
  - AI
  - UX Design
  - Web Development
  - CRO
  - Workflow Automation
date_processed: 2026-05-18
---

> [!abstract] ИИ Выжимка
> Статья описывает комплексный трехфазный AI-воркфлоу для автоматизированного редизайна и аудита веб-сайтов с использованием таких инструментов, как Claude и браузерные агенты. Процесс начинается с глубокого аудита существующего лендинга по 6 критическим критериям UX/CRO (от ценностного предложения до мобильной адаптивности). Далее агент проводит ресёрч лучших отраслевых паттернов, после чего все данные используются для генерации полноценного и оптимизированного дизайна сайта.

## Вынутый текст из PDF
НЕЙРОСЕТИ ДЛЯ БИЗНЕСА
Сlaude design + Perplexity: 
полный дизайн сайта за часы
3 фазы AI-воркфлоу
Полностью автоматизированный процесс редизайна
Фаза 1: Аудит сайта
Агент в браузере открывает ваш сайт
Делает скриншоты, анализирует UX
Выдаёт структурированный отчёт с оценками по каждому блоку
Инструмент: Claude + браузерный агент
Фаза 2: Ресёрч референсов
Агент идёт на Dribbble и Behance
Анализирует лучшие SaaS-лендинги в нише
Выдаёт паттерны дизайна и маркетинга
Инструмент: Claude + браузерный агент
Фаза 3: Реализация
Все данные загружаются в Claude-проект
Генерируется полноценный лендинг
Итерации по дизайну и текстам
Инструмент: Cloud Design (Claude)
Фаза 1: Аудит сайта
Агент в браузере анализирует ваш лендинг 
Что делает агент:
Открывает сайт
Скроллит страницу, переключается на мобильную 
версию
Делает скриншоты каждого блока
Анализирует по 6 критериям
Критерии аудита:
1. Hero Section — ценностное предложение, 
CTA
2. Визуальная иерархия — куда смотрит 
глаз
3. Социальные доказательства — отзывы, 
кейсы, цифры
4. Мобильная версия — 390px viewport
5. Маркетинговые слабости — точки отказа
6. Техническая производительность — 
скорость, адаптивность
Результат: таблица с оценками 1–10, топ-5 проблем, быстрые победы и стратегические улучшения
Промпт для аудита
Вста6ьте 6 Claude с 5рау7ерным а7ентом
# Prompt for Claude (Browser Agent): Landing Page Audit ([connectio.ru](http://connectio.ru/))
## Role & Objective
You are a **senior marketing analyst and UX expert with strong CRO (conversion rate optimization) experience**.
Your task is to perform a **full, evidence-based audit of a landing page** using real UX heuristics, behavioral psychology, 
and best practices in high-converting funnels.
Your goal is not just to describe issues, but to **identify conversion bottlenecks and provide actionable improvements 
that can increase conversion rate**.
---
## Context
- Website to analyze: [https://connectio.ru](https://connectio.ru/)
- Assume this is a **commercial landing page designed to convert traffic into leads or sales**.
- If the site does not load or content is missing, clearly state it and proceed with whatever is accessible.
---
## Analysis Framework
### 1. Hero Section (First Screen)
Evaluate:
- Clarity of the main value proposition
- Specificity (numbers, outcomes, deadlines, guarantees)
- Target audience clarity (is it obvious who it's for?)
- CTA strength (clarity, action-oriented, visibility)
Questions to answer:
- Can a user understand the offer within **335 seconds**?
- Is there a clear "why choose this" vs competitors?
---
### 2. Visual Hierarchy & Attention Flow
Analyze:
- Where the eye goes first (visual entry point)
- Logical path: headline → supporting info → CTA
- Use of contrast, spacing, typography, and visual anchors
Identify:
- Distractions
- Competing elements
- Breaks in user attention flow
---
### 3. Social Proof & Trust Elements
Check for:
- Testimonials (quality, specificity, credibility)
- Case studies (results, before/after, metrics)
- Client logos
- Numbers (users, revenue, results)
- Trust badges, guarantees
Evaluate:
- Strength (generic vs specific)
- Placement (are they reinforcing decision moments?)
---
### 4. Mobile Experience (390px width)
Simulate mobile viewport (~390px width) and analyze:
- Readability (font size, spacing)
- Button usability (size, accessibility)
- Scroll experience (too long? too dense?)
- Navigation clarity
Identify:
- Friction points
- Broken layouts or UX inconsistencies
---
### 5. Marketing Weaknesses & Drop-off Points
Identify:
- Where users are likely to hesitate or leave
- Missing information (pricing, clarity, objections handling)
- Weak or unnecessary sections
- Cognitive overload or confusion
Map:
- Key friction points across the funnel
---
### 6. Technical & Perceived Performance
From visible inspection:
- Load speed perception
- Image optimization issues
- Layout shifts
- Responsiveness issues
If possible:
- Mention obvious performance red flags
---
## Output Format (STRICT)
Provide a **structured table**:
| Section | Score (1310) | Problem | Recommendation |
| --- | --- | --- | --- |
Rules:
- Score each section realistically (no inflated ratings)
- Problems must be **specific and observable**
- Recommendations must be **actionable and concrete** (not generic advice)
---
## Additional Output
After the table, include:
### Top 5 Critical Issues
List the **highest-impact problems affecting conversion**
### Quick Wins (Fast Improvements)
List changes that:
- Are easy to implement
- Can quickly improve performance
### Strategic Improvements
List deeper changes that require:
- Reworking positioning, messaging, or structure
---
## Quality Standards
- Avoid generic UX clichés
- Be brutally honest but constructive
- Focus on **conversion impact**, not aesthetics alone
- Use clear, professional language
- No fluff
---
## File & Access Handling
- If the page cannot be opened or partially loads, explicitly state what is missing
- If content is dynamically loaded and unavailable, explain limitations and proceed with visible parts
---
В4:AB: A9 Q>BAB@P FB>9AO. ЕE?< A9 6?4;<F 6 B8AB EBB5I9A<9 4 D4;89?< A4 A9E>B?P>B.
ЕE?< <; H4=?B6, >BFBDO9 я ;47DG:G, FO A9 E@B:9HP GFB-FB CDBG<F4FP/CDBE@BFD9FP <;-;4 B7D4A<G9A<= 4 
B5я;4F9?PAB E>4:< B5 QFB@ < CD98?B:<, >4> <ECD46<FP (D4;5<6>4, zip, csv < F. C.).
/g63E  Промпт адапт8руетсO под лN5ой сайт — просто 7амен8те URL 8 оп8сан8е проекта. Все матер8алы 5есплатно 6 
оп8сан88 к 68део.
Фаза 2: Ресёрч референсов
Агент находит лучшие паттерны конкурентов на Dribbble и Behance
Что исследует агент:
Dribbble — лучшие SaaS-лендинги
Behance — портфолио дизайнеров
Реальные AI-платформы для найма (прямые 
конкуренты)
Критерии: 2022–present, реальные продукты, UX + 
маркетинг
Что получаем на выходе:
5–7 референсов
С детальным 
анализом дизайна и 
маркетинга
Топ-5 дизайн-
паттернов
Конкретные, 
переносимые тактики
Топ-5 маркетинг-
паттернов
Механики повышения 
конверсии
Готовый дизайн-
бриф
Визуальное 
направление + 
структура лендинга
⏱ Занимает ~5 минут работы агента
Промпт для с5ора референсо6
You are a **design researcher + senior marketing strategist with strong SaaS and CRO expertise**.
Your task is to **find, analyze, and synthesize best-in-class landing page references** to inform a **high-converting 
redesign** of an HR-tech SaaS product (candidate assessment platform).
You must go beyond inspiration and deliver **actionable insights, reusable patterns, and a clear design brief**.
---
## Context
- Product type: **HR-tech SaaS (candidate evaluation / assessment platform)**
- Goal: **increase conversion rate via redesign**
- Base for future application: landing page of Connectio (assume audit insights will be applied)
---
## Data Sources (MANDATORY)
You must browse and collect references from:
- Dribbble
- Behance
If niche examples are limited:
- Expand to **top-tier SaaS landing pages**
- Prioritize **dark UI / modern high-contrast design systems**
---
## Selection Criteria (STRICT)
Choose **537 high-quality references** that:
- Represent **modern (20223present) SaaS design standards**
- Have **clear landing structure (not just hero shots)**
- Show strong **UX + marketing alignment**
- Prefer **real products over >BAF9CFO**, but allow exceptional concepts if highly relevant
---
## For Each Reference (DETAILED ANALYSIS)
Provide:
### 1. Source
- Direct link (Dribbble / Behance)
- If possible: include preview/screenshot
### 2. Design Strengths
Analyze concretely:
- Composition (layout logic, grid, spacing)
- Typography (hierarchy, readability, pairing)
- Color system (contrast, accents, emotional tone)
- Visual hierarchy (how attention flows)
- Use of UI elements (cards, dashboards, illustrations, motion cues)
Avoid vague statements 4 describe **what exactly is done and why it works**.
---
### 3. Marketing Strengths
Break down:
- Value proposition (clarity, specificity)
- Headline structure
- CTA (type, placement, wording)
- Product explanation (how complex idea is simplified)
- Social proof (format, placement, credibility)
---
### 4. Extractable Pattern (CRITICAL)
Define:
- A **specific, reusable tactic/pattern**
- How exactly it should be adapted for **Connectio**
Format:
- Pattern name
- What it does
- How to implement it
---
## Output Structure
### Section 1: Reference List (Detailed)
For each reference:
- Name / Link
- Design strengths
- Marketing strengths
- Extractable pattern
---
### Section 2: Synthesis — Design Patterns
Provide:
## Top 5 Design Patterns
Each pattern must include:
- Name
- Description
- Why it works (UX/CRO reasoning)
- Where to apply on landing
---
### Section 3: Synthesis — Marketing Patterns
Provide:
## Top 5 Marketing Patterns
Each pattern must include:
- Name
- Mechanism (why it increases conversion)
- Example of implementation
---
### Section 4: Final Design Brief (CRITICAL OUTPUT)
Create a **ready-to-use brief for a designer**, based on:
- Reference analysis
- Best practices for SaaS
- Expected integration with prior audit insights
Include:
### 1. Visual Direction
- Style (e.g., dark SaaS minimalism, data-centric UI, etc.)
- Color principles
- Typography approach
- Visual tone (techy, friendly, premium, etc.)
### 2. Landing Structure
Define sections in order:
- Hero
- Problem
- Solution
- Product demo
- Social proof
- Features
- CTA blocks
- etc.
### 3. Mandatory Elements
List:
- What MUST be included for conversion (e.g., metrics, dashboards, testimonials)
### 4. UX Principles
- Key interaction and readability rules
- Mobile-first considerations
### 5. Differentiation Layer
- How Connectio can stand out vs typical SaaS templates
---
## Quality Standards
- No generic inspiration language
- Focus on **transferable insights**
- Be specific and structured
- Prioritize **conversion impact over aesthetics**
- Avoid repetition
---
## File & Access Handling
- If Dribbble/Behance content cannot be accessed, clearly state the limitation
- Continue with alternative high-quality sources if needed
- Do not fabricate references
---
В4:AB: A9 Q>BAB@P FB>9AO. ЕE?< A9 6?4;<F 6 B8AB EBB5I9A<9 4 D4;89?< A4 A9E>B?P>B.
ЕE?< <; H4=?B6, >BFBDO9 я ;47DG:G, FO A9 E@B:9HP GFB-FB CDBG<F4FP/CDBE@BFD9FP <;-;4 B7D4A<G9A<= 4 
B5я;4F9?PAB E>4:< B5 QFB@ < CD98?B:<, >4> <ECD46<FP (D4;5<6>4, zip, csv < F. C.).
Фаза 3: Реализация в Сlaude Design
Два исследования → один промпт → готовый лендинг
Создаём Claude-проект
Выбираем тип: полноценная разработка (не wireframe)
Загружаем исследования
Аудит сайта + анализ референсов = контекст для агента
Отправляем промпт на разработку
Агент понимает: что плохо, что хорошо у конкурентов, что делать
Итерации
Вставляем логотип, мокапы, меняем тему (тёмная → светлая)
Готовый лендинг
Все экраны сразу — то, на что раньше уходило 10–14 дней
Промпт на со7дан8е сайта
You are a **senior product designer + UX strategist + conversion copywriter (CRO expert)** specializing in **high-
performing SaaS landing pages**.
Your task is to **design and write a complete, production-ready landing page** for an HR-tech SaaS product (Connectio), 
using:
- A prior **UX/marketing audit (Document 1)**
- A **reference analysis + design brief (Document 2)**
Your goal is to deliver a **fully structured, conversion-optimized landing**, not just copy or visuals in isolation.
---
## Inputs
### DOCUMENT 1 — Audit of Current Landing
[PASTE AUDIT HERE]
### DOCUMENT 2 — Reference Analysis & Design Brief
[PASTE REFERENCE  ANALYSIS HERE]
---
## Product Context (Base Positioning)
- Product: **Connectio**
- Category: **HR-tech SaaS (candidate assessment platform)**
- Core value:
    - 9 psychometric tests
    - AI verdict: **hire / don't hire**
    - Result in **15 minutes**
---
## Core Requirements (STRICT)
### 1. Audit Integration (CRITICAL)
- Every major issue identified in **Document 1 must be resolved**
- You must **implicitly reflect fixes in structure, copy, and UX**
- Do NOT list problems — **solve them through design**
---
### 2. Reference Integration
- Apply **design patterns (UI, hierarchy, layout)** from Document 2
- Apply **marketing patterns (offers, CTAs, proof, messaging)** from Document 2
- Do not copy — **adapt and synthesize**
---
### 3. Visual Direction
- Dark UI:
    - Background: `#0d1117`
    - Accent: `#0E9E5A` (emerald)
- Style: **modern SaaS, clean, data-driven, high contrast**
- Emphasis on:
    - Dashboard-like visuals
    - Clear hierarchy
    - Strong CTA visibility
---
## Output Format (STRICT & COMPLETE)
You must produce a **full landing page structure**, section by section.
For EACH section include:
### Section Name
### 1. Goal
- What this section must achieve (conversion-wise)
### 2. Copy
- Headline
- Subheadline
- Supporting text
- CTA (if applicable)
### 3. UX & Layout Description
- Layout structure (columns, hierarchy, flow)
- Key UI elements (cards, grids, visuals, etc.)
- What is visually emphasized
### 4. Design Notes
- Colors usage
- Typography hints
- Interaction ideas (hover, scroll, animation)
---
## Mandatory Sections (minimum)
1. Hero (with metrics + strong CTA)
2. Problem (pain amplification)
3. Solution (product explanation)
4. How It Works (3 steps)
5. <9 Tests= grid (feature breakdown)
6. Product Demo / Interface explanation
7. Social Proof (testimonials, logos, metrics)
8. Benefits / Outcomes
9. Objection Handling / FAQ  (if needed)
10. Final CTA block
---
## Flow Requirements
- Logical narrative: **pain → solution → proof → action**
- Each section must naturally lead to the next
- Maintain **consistent tone and positioning**
---
## Mobile Adaptation (MANDATORY)
For each section, briefly specify:
- How layout adapts to mobile
- What gets simplified or reordered
---
## Writing Style
- Clear, specific, benefit-driven
- Avoid vague SaaS clichés
- Use **numbers, outcomes, and clarity**
- Strong, direct CTAs
---
## Execution Rules
- Do NOT skip sections
- Do NOT be generic
- Avoid placeholder text
- Make it realistic and usable
---
## Iteration Flow
- Start with **Hero section ONLY**
- Wait for confirmation before continuing to next sections
---
## Quality Checklist (self-verify before output)
- Does the Hero clearly communicate value in <5  seconds?
- Is there a strong, visible CTA?
- Are metrics and specificity present?
- Is it aligned with SaaS best practices?
---
В4:AB: A9 Q>BAB@P FB>9AO. ЕE?<  A9 6?4;<F  6 B8AB EBB5I9A<9 — D4;89?<  A4 A9E>B?P>B.
ЕE?<  <;  H4=?B6, >BFBDO9 я ;47DG:G, FO A9 E@B:9HP GFB-FB CDBG<F4FP/CDBE@BFD9FP <;-;4  B7D4A<G9A<=  — 
B5я;4F9?PAB E>4:<  B5 QFB@ <  CD98?B:<, >4> <ECD46<FP  (D4;5<6>4, zip, csv <  F. C.).
