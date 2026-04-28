#!/usr/bin/env python3
"""
Copilot Task Processor v1.0

Мониторит _TASKS/ и _FLAGS/ папки.
Автоматически обрабатывает новые задачи от Антигравити.
Пишет результаты в FROM_CHATGPT.md и архивирует обработанные файлы.

Запуск:
  python scripts/task_processor.py
"""

import sys
import time
import json
import logging
from pathlib import Path
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [PROCESSOR] %(levelname)s - %(message)s'
)
logger = logging.getLogger("task_processor")

# Paths
BASE = Path(__file__).parent.parent.resolve()
TASKS_DIR = BASE / "_TASKS"
FLAGS_DIR = BASE / "_FLAGS"
AI_EXCHANGE = BASE / "obsidian_brain/_AI_EXCHANGE"
FROM_FILE = AI_EXCHANGE / "FROM_CHATGPT.md"
ARCHIVE_DIR = BASE / "archive/processed_tasks"

ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)


class TaskProcessor:
    """Обрабатывает задачи из _TASKS папки."""
    
    def __init__(self):
        self.processed = set()
    
    def get_pending_tasks(self):
        """Получить список ожидающих задач."""
        if not TASKS_DIR.exists():
            return []
        
        tasks = []
        for task_file in sorted(TASKS_DIR.glob("*.yaml")) + sorted(TASKS_DIR.glob("*.json")):
            if task_file.name not in self.processed:
                try:
                    tasks.append(self._load_task(task_file))
                except Exception as e:
                    logger.error(f"Failed to load {task_file}: {e}")
        return tasks
    
    def _load_task(self, path: Path) -> dict:
        """Загрузить задачу из файла."""
        import yaml
        content = path.read_text(encoding='utf-8')
        
        if path.suffix == '.yaml':
            return yaml.safe_load(content) or {}
        elif path.suffix == '.json':
            return json.loads(content)
        return {}
    
    def process_task(self, task: dict, task_path: Path):
        """Обработать одну задачу."""
        logger.info(f"📋 Processing task: {task.get('title', 'Unknown')}")
        
        # Формируем ответ
        response = f"""
# Task Processed: {task.get('title', 'Unknown')}
**Status**: Received and catalogued  
**Timestamp**: {datetime.now().isoformat()}  
**Priority**: {task.get('priority', 'medium')}  

## Details
{task.get('description', 'No description')}

## Next Steps
1. Auto-categorized and stored in archive
2. Ready for Antigraviti review
3. Can be assigned to specific workflow
"""
        
        # Сохраняем в FROM_CHATGPT.md
        self._append_to_exchange(response)
        
        # Архивируем обработанный файл
        archive_path = ARCHIVE_DIR / f"{task_path.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{task_path.suffix}"
        task_path.rename(archive_path)
        
        self.processed.add(task_path.name)
        logger.info(f"✅ Task archived: {archive_path}")
    
    def _append_to_exchange(self, content: str):
        """Добавить контент в FROM_CHATGPT.md."""
        if FROM_FILE.exists():
            existing = FROM_FILE.read_text(encoding='utf-8')
            FROM_FILE.write_text(existing + "\n\n" + content, encoding='utf-8')
        else:
            FROM_FILE.write_text(content, encoding='utf-8')
    
    def check_flags(self):
        """Проверить флаги для специальных действий."""
        if not FLAGS_DIR.exists():
            return
        
        for flag in FLAGS_DIR.glob("*"):
            if flag.name == ".refresh_knowledge":
                logger.info("🔄 Refreshing knowledge base...")
                # TODO: Подключить refresh logic
                flag.unlink()
            
            elif flag.name == ".sync_obsidian":
                logger.info("📚 Syncing Obsidian...")
                # TODO: Подключить sync logic
                flag.unlink()
            
            elif flag.name == ".run_tests":
                logger.info("🧪 Running tests...")
                # TODO: Подключить test logic
                flag.unlink()
            
            elif flag.name == ".reboot":
                logger.warning("🚀 REMOTE REBOOT TRIGGERED!")
                import os
                os.system("shutdown /r /t 10 /c \"MASTADONT: Remote reboot in 10 seconds...\"")
                flag.unlink()

            elif flag.name == ".shutdown":
                logger.warning("🛑 REMOTE SHUTDOWN TRIGGERED!")
                import os
                os.system("shutdown /s /t 10 /c \"MASTADONT: Remote shutdown in 10 seconds...\"")
                flag.unlink()
    
    def run(self):
        """Главный цикл обработки."""
        logger.info("=" * 50)
        logger.info("🟢 Copilot Task Processor v1.0 started")
        logger.info("=" * 50)
        
        while True:
            try:
                # Проверяем флаги
                self.check_flags()
                
                # Обрабатываем задачи
                tasks = self.get_pending_tasks()
                for task_file in sorted(TASKS_DIR.glob("*.yaml")) + sorted(TASKS_DIR.glob("*.json")):
                    if task_file.name not in self.processed:
                        try:
                            task = self._load_task(task_file)
                            self.process_task(task, task_file)
                        except Exception as e:
                            logger.error(f"Error processing {task_file}: {e}")
                
                time.sleep(10)
            
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                time.sleep(10)


if __name__ == "__main__":
    processor = TaskProcessor()
    processor.run()
