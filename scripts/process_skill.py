import sys
import os

input_file = "schemes_response.txt"
output_dir = os.path.join(os.environ['USERPROFILE'], 'Downloads', 'NotebookLM', '.agents', 'skills', 'ai_business_schemes')
output_file = os.path.join(output_dir, "SKILL.md")

os.makedirs(output_dir, exist_ok=True)

try:
    with open(input_file, "r", encoding="cp1251", errors="replace") as f:
        content = f.read()

    skill_template = f"""---
name: ai_business_schemes
description: "Руководство по запуску 3-х бизнес-схем на базе ИИ из видео (YouTube 2.0, PDF-воронки, B2B AI-агентства)."
---

# 🤖 AI Business Schemes 2026 (From YouTube Video)

Этот навык основан на выжимке из видео про самый ленивый заработок на ИИ в 2026 году.

## 📄 Raw Extracted Content from NotebookLM
{content}

---

## 🛠 Instructions for AntiGravity (The Builder)
When triggered, AntiGravity should use the schemes above to help the user build their business. For example:
- **For Scheme 1 (YouTube Shorts/Reels):** Suggest generating scripts via `notebook_query` and writing an automation to combine them with ElevenLabs APIs.
- **For Scheme 2 (PDF Funnels):** Ask the user for a topic, use NotebookLM to generate a deep-dive, then use AntiGravity to convert it into a well-formatted PDF and build a simple Telegram bot for the funnel.
- **For Scheme 3 (B2B AI Agencies):** Propose searching for local businesses, extracting their info, and using NotebookLM to generate personalized pitches.

"""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(skill_template)
    print(f"Skill saved successfully to {output_file}")
except Exception as e:
    print(f"Error: {e}")
