import re
import sys
import urllib.parse
import zipfile
import httpx
from pathlib import Path

# Устанавливаем UTF-8 для вывода в консоль Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Конфигурация путей
CONTENT_FILE = Path(r"C:\Users\Sasha  Baron\.gemini\antigravity\brain\c73fe980-485b-433b-bbdd-e57bd93eac81\.system_generated\steps\6724\content.md")
CLIPPINGS_DIR = Path(r"C:\ANTIGRAVITY\1\obsidian_brain\1_PROJECTS\Clippings")

def setup_dirs():
    CLIPPINGS_DIR.mkdir(parents=True, exist_ok=True)

def get_download_url(public_url: str) -> dict:
    """Запрашивает у Яндекса прямую ссылку на скачивание/информацию."""
    # Кодируем ссылку
    encoded_url = urllib.parse.quote(public_url)
    
    # 1. Запрашиваем информацию о ресурсе
    info_api = f"https://cloud-api.yandex.net/v1/disk/public/resources?public_key={encoded_url}"
    try:
        with httpx.Client(timeout=30.0, follow_redirects=True) as client:
            r = client.get(info_api)
            r.raise_for_status()
            res_data = r.json()
            return res_data
    except Exception as e:
        print(f"Ошибка получения инфо по {public_url}: {e}")
        return None

def download_file(direct_url: str, filename: str) -> Path:
    """Скачивает файл по прямой ссылке."""
    dest_path = CLIPPINGS_DIR / filename
    print(f"Скачивание: {filename}...")
    try:
        with httpx.Client(timeout=120.0, follow_redirects=True) as client:
            with client.stream("GET", direct_url) as response:
                response.raise_for_status()
                with open(dest_path, "wb") as f:
                    for chunk in response.iter_bytes():
                        f.write(chunk)
        print(f"Успешно скачан: {filename}")
        return dest_path
    except Exception as e:
        print(f"Ошибка скачивания {filename}: {e}")
        return None

def handle_zip(filepath: Path):
    """Распаковывает ZIP-файлы в Clippings и удаляет исходный ZIP."""
    if zipfile.is_zipfile(filepath):
        print(f"Распаковка {filepath.name}...")
        try:
            with zipfile.ZipFile(filepath, 'r') as zip_ref:
                zip_ref.extractall(CLIPPINGS_DIR)
            filepath.unlink() # Удаляем архив после распаковки
            print(f"Успешно распакован и удален: {filepath.name}")
        except Exception as e:
            print(f"Ошибка распаковки {filepath.name}: {e}")

def process_yandex_resource(public_url: str):
    """Обрабатывает ресурс (файл или папку) по ссылке Яндекс Диска."""
    data = get_download_url(public_url)
    if not data:
        return

    res_type = data.get("type", "file")
    
    if res_type == "file":
        # Скачиваем одиночный файл
        file_url = data.get("file")
        name = data.get("name", "downloaded_file")
        if file_url:
            path = download_file(file_url, name)
            if path and path.suffix.lower() == ".zip":
                handle_zip(path)
    elif res_type == "dir":
        # Скачиваем файлы из папки
        print(f"Обнаружена папка: {data.get('name')}")
        embedded = data.get("_embedded", {})
        items = embedded.get("items", [])
        for item in items:
            if item.get("type") == "file":
                file_url = item.get("file")
                name = item.get("name", "downloaded_file")
                if file_url:
                    path = download_file(file_url, name)
                    if path and path.suffix.lower() == ".zip":
                        handle_zip(path)

def extract_links_from_md() -> list:
    """Извлекает все Яндекс Диск ссылки из content.md."""
    if not CONTENT_FILE.exists():
        print(f"Файл {CONTENT_FILE} не найден.")
        return []
        
    with open(CONTENT_FILE, "r", encoding="utf-8") as f:
        text = f.read()
        
    # Ищем ссылки вида https://disk.yandex.ru/d/... или /i/...
    links = re.findall(r"https://disk\.yandex\.ru/[id]/[A-Za-z0-9_-]+", text)
    # Возвращаем уникальные ссылки
    return list(set(links))

def main():
    setup_dirs()
    print("Поиск ссылок на материалы...")
    links = extract_links_from_md()
    
    if not links:
        print("Ссылки не найдены.")
        return
        
    print(f"Найдено уникальных ссылок на материалы: {len(links)}")
    
    print(f"Запускаем скачивание всех {len(links)} ссылок...")
    
    for link in links:
        print(f"\nОбработка ссылки: {link}")
        process_yandex_resource(link)
        
    print("\nСкачивание материалов завершено!")

if __name__ == "__main__":
    main()
