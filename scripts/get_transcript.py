import subprocess
import os

def save_transcript(video_id: str, output_file: str = "transcript.txt") -> None:
    print(f"Попытка получить транскрипт через CLI для {video_id}...")
    
    # Команда: python -m youtube_transcript_api <video_id> --languages ru en
    cmd = [
        "C:/Program Files/PyManager/python.exe", 
        "-m", "youtube_transcript_api", 
        video_id, 
        "--languages", "ru", "en"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        if result.returncode == 0:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(result.stdout)
            print(f"Успех! Сохранено в {output_file}")
        else:
            print(f"Ошибка CLI: {result.stderr}")
    except Exception as e:
        print(f"Системная ошибка: {e}")

if __name__ == "__main__":
    save_transcript("CKrI-Q15FbU")

if __name__ == "__main__":
    save_transcript("CKrI-Q15FbU")
