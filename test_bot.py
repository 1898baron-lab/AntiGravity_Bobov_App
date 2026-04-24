#!/usr/bin/env python3
"""
Test script for telegram_bot.py logic
"""

import os
import sys
import json

# Add project root to path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from dotenv import load_dotenv

# Load env
load_dotenv(os.path.join(BASE_DIR, ".env"))
BOT_TOKEN = os.getenv("BOT_TOKEN")

print("=== Telegram Bot Test ===")
print(f"BASE_DIR: {BASE_DIR}")
print(f"BOT_TOKEN exists: {bool(BOT_TOKEN)}")

# Test sessions
SESSIONS_FILE = os.path.join(BASE_DIR, "user_sessions.json")
print(f"Sessions file: {SESSIONS_FILE}")

# Test paths
skill_path = os.path.join(BASE_DIR, ".agents", "skills", "legal_expert_bobov", "SKILL.md")
brief_path = os.path.join(BASE_DIR, "obsidian_brain", "_AI_EXCHANGE", "legal_attack_brief.md")

print(f"Skill path exists: {os.path.exists(skill_path)}")
print(f"Brief path exists: {os.path.exists(brief_path)}")

# Test git repo
git_dir = os.path.join(BASE_DIR, ".git")
print(f"Git repo exists: {os.path.exists(git_dir)}")

print("=== Test Complete ===")