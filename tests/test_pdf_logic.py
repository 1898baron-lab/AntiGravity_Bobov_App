import pytest
import os
import sys

# Добавляем корень проекта в sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

def test_prompts_structure():
    """Проверяем, что все промпты имеют нужные ключи."""
    from scripts.prompts_data import PROMPTS

    required_keys = ["num", "title", "task", "prompt", "tools", "tip"]

    assert len(PROMPTS) == 10, f"Ожидалось 10 промптов, получено {len(PROMPTS)}"
    for p in PROMPTS:
        for key in required_keys:
            assert key in p, f"Ключ '{key}' отсутствует в промпте #{p.get('num')}"
            assert isinstance(p[key], str), f"Значение '{key}' должно быть строкой"
            assert len(p[key]) > 0, f"Значение '{key}' не должно быть пустым"

def test_prompt_numbers_unique():
    """Проверяем, что номера промптов уникальны."""
    from scripts.prompts_data import PROMPTS
    nums = [p["num"] for p in PROMPTS]
    assert len(nums) == len(set(nums)), "Найдены дублирующиеся номера промптов"
