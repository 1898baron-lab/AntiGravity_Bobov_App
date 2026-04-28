"""
MASTODONT Agent Core v0.1 — Central Intelligence & Orchestration
=============================================================
Implementation of the structured pipeline:
Task -> Plan -> Execution -> Verification -> Recording

This core centralizes decision making and ensures traceability.
"""

import os
import json
import logging
from pathlib import Path
from datetime import datetime
from scripts.verifier import MastodontVerifier

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s [CORE] %(levelname)s - %(message)s')
logger = logging.getLogger("agent_core")

class AgentCore:
    def __init__(self, workspace_root: str):
        self.root = Path(workspace_root)
        self.inbox = self.root / "obsidian_brain/_AI_EXCHANGE/TO_CHATGPT.md"
        self.outbox = self.root / "obsidian_brain/_AI_EXCHANGE/FROM_CHATGPT.md"
        self.plan_file = self.root / "obsidian_brain/_AI_EXCHANGE/AGENT_PLAN.md"
        self.verifier = MastodontVerifier()
        
    async def process_cycle(self):
        """Полный цикл обработки задачи."""
        # 1. TASK: Читаем входящую задачу
        task = self._read_task()
        if not task:
            return
            
        logger.info("New task detected. Starting structured cycle.")

        # 2. PLAN: Формируем план действий (Step-by-step)
        plan = self._generate_plan(task)
        self._record_plan(plan)
        logger.info("Plan generated and recorded.")

        # 3. EXECUTION: Выполнение (Поиск НТД, расчеты)
        results = await self._execute(plan)
        logger.info("Execution complete.")

        # 4. VERIFICATION: Проверка фактов и НТД
        verified_data = await self._verify(results)
        logger.info("Verification complete.")

        # 5. RECORDING: Запись в Obsidian с трассировкой
        self._record_final_response(verified_data)
        logger.info("Cycle complete. Response recorded.")

    def _read_task(self) -> str:
        if self.inbox.exists():
            return self.inbox.read_text(encoding="utf-8").strip()
        return ""

    def _generate_plan(self, task: str) -> dict:
        # Здесь будет логика LLM для декомпозиции
        return {
            "steps": [
                "Идентификация ключевых стандартов (ГОСТ/ISO)",
                "Проверка допусков по таблицам",
                "Анализ материаловедческой совместимости",
                "Оценка рисков деформации"
            ],
            "timestamp": datetime.now().isoformat()
        }

    def _record_plan(self, plan: dict):
        content = "# 📝 Текущий план агента\n\n"
        for i, step in enumerate(plan["steps"], 1):
            content += f"{i}. {step}\n"
        self.plan_file.write_text(content, encoding="utf-8")

    async def _execute(self, plan: dict) -> dict:
        import httpx
        logger.info("Executing task via ChatGPT Connector...")
        
        # Берем саму задачу из входного файла (для теста)
        task_text = self._read_task()
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    "http://localhost:8001/v1/messages",
                    json={"prompt": task_text}
                )
                if response.status_code == 200:
                    answer = response.json().get("response", "")
                    return {"raw_data": answer}
                else:
                    return {"raw_data": f"Error: Connector returned status {response.status_code}"}
        except Exception as e:
            return {"raw_data": f"Error connecting to ChatGPT Bridge: {e}"}

    async def _verify(self, results: dict) -> dict:
        # Слой верификации: проверка ссылок и уверенности
        raw_text = results.get("raw_data", "")
        report = await self.verifier.verify(raw_text)
        return {
            "data": results,
            "report": report
        }

    def _record_final_response(self, verified_data: dict):
        report = verified_data["report"]
        result_text = verified_data["data"].get("raw_data", "No data")
        
        status_tag = "#verified" if report['status'] == "verified" else "#unverified"
        content = f"""# 📑 Engineering Audit Report
---
date: {datetime.now().strftime('%Y-%m-%d %H:%M')}
confidence: {report['confidence']}%
status: {status_tag}
---

## 🛠 Analysis Results
{result_text}

## 🛡 Verification Audit Findings
"""
        for finding in report['findings']:
            content += f"- {finding}\n"
            
        # Записываем в папку Tasks в Obsidian
        filename = f"audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        output_path = self.root / "obsidian_brain/Tasks" / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding="utf-8")
        
        # Также обновляем FROM_CHATGPT.md для обратной связи
        self.outbox.write_text(content, encoding="utf-8")

if __name__ == "__main__":
    # В будущем: запуск через asyncio.run(core.process_cycle())
    logger.info("Agent Core initialized. Ready for orchestration.")
