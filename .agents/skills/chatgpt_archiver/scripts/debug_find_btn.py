import asyncio
from playwright.async_api import async_playwright
import sys

if sys.stdout.encoding != 'utf-8':
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

async def find_more_btn():
    async with async_playwright() as pw:
        browser = await pw.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = browser.contexts[0]
        page = context.pages[0]

        print("[INFO] Searching for 'More' button via JS text scan...")

        # Ищем ЛЮБОЙ элемент с текстом похожим на кнопку "Больше"
        result = await page.evaluate("""
            () => {
                const all = document.querySelectorAll('*');
                const found = [];
                for (const el of all) {
                    const txt = el.innerText || el.textContent || '';
                    const trimmed = txt.trim();
                    // Ищем элементы у которых текст короткий и похож на кнопку "Больше"
                    if (trimmed.length < 30 && 
                        (trimmed.toLowerCase().includes('больше') || 
                         trimmed.toLowerCase().includes('more') ||
                         trimmed.toLowerCase().includes('ещё') ||
                         trimmed.toLowerCase().includes('показать') ||
                         trimmed.toLowerCase().includes('see more')
                        ) &&
                        el.children.length < 3) {
                        const rect = el.getBoundingClientRect();
                        found.push({
                            tag: el.tagName,
                            text: trimmed,
                            x: Math.round(rect.x),
                            y: Math.round(rect.y),
                            w: Math.round(rect.width),
                            h: Math.round(rect.height),
                            className: el.className.substring(0, 80),
                            id: el.id,
                            role: el.getAttribute('role') || '',
                            ariaLabel: el.getAttribute('aria-label') || ''
                        });
                    }
                }
                return found;
            }
        """)
        
        print(f"\n[RESULT] Found {len(result)} candidate elements:")
        for el in result:
            print(f"  <{el['tag']}> text='{el['text']}' | y={el['y']} x={el['x']} | role='{el['role']}' | aria='{el['ariaLabel']}' | class='{el['className']}'")

        print("\n[INFO] Elements in y=680..780 range (where 'Больше' should be):")
        all_els = await page.evaluate("""
            () => {
                const all = document.querySelectorAll('nav *');
                const found = [];
                for (const el of all) {
                    const rect = el.getBoundingClientRect();
                    if (rect.y > 680 && rect.y < 780 && rect.width > 20 && rect.height > 10) {
                        found.push({
                            tag: el.tagName,
                            text: (el.innerText || '').trim().substring(0, 50),
                            x: Math.round(rect.x),
                            y: Math.round(rect.y),
                            w: Math.round(rect.width),
                            h: Math.round(rect.height),
                            className: el.className.substring(0, 80),
                            role: el.getAttribute('role') || ''
                        });
                    }
                }
                return found;
            }
        """)
        
        print(f"  Found {len(all_els)} elements:")
        for el in all_els:
            print(f"  <{el['tag']}> text='{el['text']}' | y={el['y']} x={el['x']} w={el['w']} | role='{el['role']}' | class='{el['className']}'")

asyncio.run(find_more_btn())
