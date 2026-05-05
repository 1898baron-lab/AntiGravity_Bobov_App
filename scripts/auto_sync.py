import os
import subprocess
import time
import logging
from datetime import datetime

# Настройка логов
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', filename='auto_sync.log')

PROJECT_PATH = "C:/ANTIGRAVITY/1"
SYNC_INTERVAL = 30  # Интервал проверки в секундах

def run_git_sync():
    try:
        # Проверяем статус
        status = subprocess.check_output(["git", "status", "--short"], cwd=PROJECT_PATH).decode().strip()
        
        if status:
            logging.info(f"Detected changes: {status[:100]}...")
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Syncing changes...")
            
            subprocess.run(["git", "add", "."], cwd=PROJECT_PATH)
            subprocess.run(["git", "commit", "-m", "auto: synchronization update"], cwd=PROJECT_PATH)
            subprocess.run(["git", "push", "origin", "main"], cwd=PROJECT_PATH)
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Sync complete.")
        else:
            # logging.info("No changes detected.")
            pass
            
    except Exception as e:
        logging.error(f"Sync error: {e}")
        print(f"Error during sync: {e}")

if __name__ == "__main__":
    print("=== AntiGravity Auto-Sync Autopilot Started ===")
    print(f"Watching: {PROJECT_PATH}")
    print(f"Interval: {SYNC_INTERVAL}s")
    
    while True:
        run_git_sync()
        time.sleep(SYNC_INTERVAL)
