import asyncio
import httpx
from pydantic import BaseModel
from typing import List

class BOMItem(BaseModel):
    name: str
    material: str
    quantity: int
    notes: str

async def generate_bom_arena_ai(project_name: str) -> List[BOMItem]:
    """
    Заглушка для генерации Bill of Materials через API Arena.ai.
    Использует httpx для асинхронных запросов и pydantic для валидации.
    """
    print(f"[Arena.ai Designer] Формирование промпта для проекта: {project_name}")
    prompt = f"""
    Роль: Ведущий инженер-конструктор.
    Задача: Разработать техническую спецификацию и BOM (Bill of Materials) для проекта {project_name}.
    Требования: Указать детали, материалы по ГОСТ и количество. Формат JSON.
    """
    
    print("[Arena.ai Designer] Симуляция запроса к API (kimi-k2-thinking-turbo)...")
    await asyncio.sleep(2) # Симуляция сетевой задержки
    
    # Пример успешного ответа
    fake_response = [
        {"name": "Основание", "material": "Сталь Ст3", "quantity": 1, "notes": "Лазерная резка"},
        {"name": "Крепежный болт М10", "material": "Сталь 20", "quantity": 8, "notes": "Оцинкованный"}
    ]
    
    # Валидация через Pydantic
    bom = [BOMItem(**item) for item in fake_response]
    return bom

if __name__ == "__main__":
    async def main():
        bom = await generate_bom_arena_ai("Модульный Мангал v2")
        print("\n=== Результат BOM ===")
        for item in bom:
            print(f"- {item.name} ({item.material}) x{item.quantity} [{item.notes}]")

    asyncio.run(main())
