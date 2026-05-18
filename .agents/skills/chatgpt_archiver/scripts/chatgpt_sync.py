import asyncio
from playwright.async_api import async_playwright
import os
import re
import sys

if sys.stdout.encoding != 'utf-8':
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

async def expand_all_projects(page):
    """Кликаем кнопку 'Больше' в секции Проекты чтобы раскрыть все проекты."""
    print("[INFO] Ищем кнопку 'Больше' в секции Проекты (y>500)...")
    
    clicked = await page.evaluate("""
        () => {
            // Находим все div с классом menu-item содержащие текст 'Больше'
            const divs = document.querySelectorAll('div.group.__menu-item, div.__menu-item');
            for (const el of divs) {
                const txt = (el.innerText || '').trim();
                const rect = el.getBoundingClientRect();
                // Берем только тот что в секции Проекты (y > 500, не GPTs)
                if (txt === 'Больше' && rect.y > 500) {
                    console.log('Found Больше at y=' + rect.y);
                    el.click();
                    return true;
                }
            }
            // Fallback: ищем по LI list-none содержащему 'Больше'
            const lis = document.querySelectorAll('li.list-none');
            for (const li of lis) {
                const txt = (li.innerText || '').trim();
                const rect = li.getBoundingClientRect();
                if (txt === 'Больше' && rect.y > 500) {
                    console.log('Found LI Больше at y=' + rect.y);
                    li.click();
                    return true;
                }
            }
            return false;
        }
    """)
    
    if clicked:
        print("  [OK] Кнопка 'Больше' нажата! Ждем загрузки проектов...")
        await asyncio.sleep(3)
    else:
        print("  [WARN] Кнопка 'Больше' не найдена — продолжаем без неё")

async def scroll_and_collect_projects(page):
    """Прокручиваем боковое меню и собираем все проекты."""
    print("[INFO] Сбор всех проектов из бокового меню...")
    
    all_projects = {}
    
    # Несколько прокруток меню
    for scroll_attempt in range(15):
        sidebar = await page.query_selector('nav')
        if sidebar:
            await sidebar.evaluate("el => el.scrollTop += 300")
        await asyncio.sleep(0.5)
        
        # Собираем ссылки на проекты (формат /g/g-p-...)
        links = await page.query_selector_all('a[href*="/g/g-p-"]')
        for link in links:
            href = await link.get_attribute('href')
            title = (await link.inner_text()).strip().split("\n")[0]
            if href and title and href not in all_projects:
                all_projects[href] = {"title": title, "url": f"https://chatgpt.com{href}"}
                print(f"  [+] {title}")
    
    # Также широкий поиск
    links2 = await page.query_selector_all('a[href*="/g/g-"]')
    for link in links2:
        href = await link.get_attribute('href')
        title = (await link.inner_text()).strip().split("\n")[0]
        if href and title and href not in all_projects:
            all_projects[href] = {"title": title, "url": f"https://chatgpt.com{href}"}
            print(f"  [+] (wide) {title}")
    
    return list(all_projects.values())

async def deep_project_sync_cdp():
    print("[INIT] ChatGPT Projects Sync v8 - CDP connection...")
    async with async_playwright() as pw:
        try:
            browser = await pw.chromium.connect_over_cdp("http://127.0.0.1:9222")
        except Exception as e:
            print(f"[ERR] Cannot connect to browser on port 9222: {e}")
            print("      Make sure Chrome is running with --remote-debugging-port=9222")
            return
            
        context = browser.contexts[0]
        page = context.pages[0] if context.pages else await context.new_page()
        
        output_parent = r"C:\ANTIGRAVITY\1\obsidian_brain\4_ARCHIVE\ChatGPT_Projects"
        os.makedirs(output_parent, exist_ok=True)
        
        # Переходим на главную страницу ChatGPT
        print("[INFO] Navigating to chatgpt.com...")
        await page.goto("https://chatgpt.com/", timeout=60000)
        await asyncio.sleep(5)
        
        # Нажимаем кнопку "Больше" чтобы раскрыть все проекты
        await expand_all_projects(page)
        
        # Прокручиваем и собираем все проекты
        projects = await scroll_and_collect_projects(page)
        print(f"\n[INFO] Total unique projects found: {len(projects)}")
        
        if len(projects) == 0:
            print("[ERR] No projects found. Try scrolling the sidebar manually and re-run.")
            return

        for project in projects:
            p_title = re.sub(r'[^\w\s\-]', '_', project['title'])[:80]
            print(f"\n[SYNC] Processing: {p_title}")
            p_dir = os.path.join(output_parent, p_title)
            os.makedirs(p_dir, exist_ok=True)
            
            # Переходим на страницу проекта
            proj_url = project['url']
            if not proj_url.endswith('/project'):
                proj_url = proj_url.rstrip('/') + '/project'
            
            try:
                await page.goto(proj_url, timeout=60000)
                await asyncio.sleep(4)
            except Exception as e:
                print(f"  [WARN] Can't open project page: {e}")
                continue
            
            # Собираем чаты в проекте
            chat_links = await page.query_selector_all('a[href*="/c/"]')
            chats_to_download = []
            
            for cl in chat_links:
                try:
                    box = await cl.bounding_box()
                    if box and box['x'] > 100:
                        c_title = (await cl.inner_text()).split("\n")[0].strip()
                        c_href = await cl.get_attribute('href')
                        if c_title and c_href and '/c/' in c_href:
                            chats_to_download.append({
                                "title": c_title,
                                "url": f"https://chatgpt.com{c_href}"
                            })
                except:
                    continue
            
            # Убираем дубли
            seen = set()
            unique_chats = []
            for c in chats_to_download:
                if c['url'] not in seen:
                    seen.add(c['url'])
                    unique_chats.append(c)
            
            print(f"  [INFO] Found {len(unique_chats)} chats in project")
            
            # Сохраняем оглавление
            toc_path = os.path.join(p_dir, f"00_INDEX_{p_title}.md")
            with open(toc_path, "w", encoding="utf-8") as f:
                f.write(f"# Project: {project['title']}\n\n")
                for c in unique_chats:
                    f.write(f"- {c['title']}\n")
            
            # Скачиваем каждый чат
            for chat in unique_chats:
                fname = re.sub(r'[^\w\s\-]', '_', chat['title']).strip()[:100] + ".md"
                fpath = os.path.join(p_dir, fname)
                
                if os.path.exists(fpath) and os.path.getsize(fpath) > 200:
                    print(f"  [SKIP] Already downloaded: {chat['title']}")
                    continue
                    
                print(f"  [CHAT] Downloading: {chat['title']}")
                try:
                    await page.goto(chat['url'], timeout=30000)
                    await page.wait_for_selector('[data-message-author-role]', timeout=20000)
                    await asyncio.sleep(2)
                    
                    messages = await page.query_selector_all('[data-message-author-role]')
                    content = f"# {chat['title']}\n\n"
                    for msg in messages:
                        role = await msg.get_attribute('data-message-author-role')
                        txt = await msg.inner_text()
                        content += f"### {role.upper()}\n{txt}\n\n"
                    
                    with open(fpath, "w", encoding="utf-8") as f:
                        f.write(content)
                    print(f"  [OK] Saved ({len(messages)} messages)")
                except Exception as e:
                    print(f"  [ERR] {e}")
                    continue
        
        print(f"\n[DONE] Sync complete! Files saved to: {output_parent}")

if __name__ == "__main__":
    asyncio.run(deep_project_sync_cdp())
