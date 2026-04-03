import json
import os

def find_sub_url(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Сначала ищем manual subtitles
    subs = data.get('subtitles', {})
    # Потом automatic captions
    auto_subs = data.get('automatic_captions', {})
    
    target_lang = None
    if 'ru' in subs: target_lang = subs['ru']
    elif 'ru' in auto_subs: target_lang = auto_subs['ru']
    elif 'en' in subs: target_lang = subs['en']
    elif 'en' in auto_subs: target_lang = auto_subs['en']
    
    if not target_lang:
        return None
    
    # Ищем формат vtt или srv1
    for fmt in target_lang:
        if fmt.get('ext') == 'vtt':
            return fmt.get('url')
        if fmt.get('ext') == 'srv1':
            return fmt.get('url')
            
    return target_lang[0].get('url') if target_lang else None

if __name__ == "__main__":
    url = find_sub_url("C:/ANTIGRAVITY/1/video_info.json")
    if url:
        print(url)
    else:
        print("URL NOT FOUND")
