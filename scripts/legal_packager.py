import os
import json
import markdown
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle, PageBreak
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import urllib.request

# ─── Конфигурация путей ───────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(__file__)
BRAIN_DIR = os.path.join(os.environ['USERPROFILE'], ".gemini", "antigravity", "brain", "564d462c-7ee0-4e05-abc9-5b2bb2a5af01")
DOCS_DIR = BASE_DIR
OUTPUT_DIR = os.path.join(BASE_DIR, "legal_dossier_output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─── Файлы для сборки ─────────────────────────────────────────────────────────
FILES = [
    {"title": "ОТЧЕТ ДЛЯ ОТЦА", "path": os.path.join(BRAIN_DIR, "report_for_father.md"), "type": "md"},
    {"title": "ФИНАЛЬНАЯ ЖАЛОБА В ПРОКУРАТУРУ", "path": os.path.join(DOCS_DIR, "complaint_prosecutor_final.txt"), "type": "txt"},
    {"title": "ПРАВОВЫЕ АРГУМЕНТЫ И ПРАКТИКА", "path": os.path.join(BRAIN_DIR, "legal_arguments_practice.md"), "type": "md"},
    {"title": "ИНСТРУКЦИЯ ПО ПОДАЧЕ", "path": os.path.join(BRAIN_DIR, "how_to_file_instruction.md"), "type": "md"},
    {"title": "ШАБЛОН ОПИСИ ИМУЩЕСТВА", "path": os.path.join(BRAIN_DIR, "property_inventory_template.md"), "type": "md"},
]

# ─── Шрифты (DejaVu для кириллицы) ───────────────────────────────────────────
FONT_DIR = os.path.join(BASE_DIR, "fonts")
os.makedirs(FONT_DIR, exist_ok=True)

FONTS = {
    "DejaVu":       "https://cdn.jsdelivr.net/npm/dejavu-fonts-ttf@2.37.3/ttf/DejaVuSans.ttf",
    "DejaVu-Bold":  "https://cdn.jsdelivr.net/npm/dejavu-fonts-ttf@2.37.3/ttf/DejaVuSans-Bold.ttf",
}

for name, url in FONTS.items():
    font_path = os.path.join(FONT_DIR, f"{name}.ttf")
    if not os.path.exists(font_path):
        urllib.request.urlretrieve(url, font_path)
    pdfmetrics.registerFont(TTFont(name, font_path))

# ─── Сборка PDF ───────────────────────────────────────────────────────────────
def generate_pdf():
    output_pdf = os.path.join(OUTPUT_DIR, "legal_dossier_bobov.pdf")
    doc = SimpleDocTemplate(output_pdf, pagesize=A4, margin=2*cm)
    styles = getSampleStyleSheet()
    
    sH1 = ParagraphStyle("sH1", fontName="DejaVu-Bold", fontSize=18, spaceAfter=12, textColor=colors.HexColor("#1A3C5E"))
    sBody = ParagraphStyle("sBody", fontName="DejaVu", fontSize=10, leading=14, spaceAfter=8)
    sTitle = ParagraphStyle("sTitle", fontName="DejaVu-Bold", fontSize=24, alignment=1, spaceAfter=40)

    story = [
        Spacer(1, 5*cm),
        Paragraph("ЮРИДИЧЕСКОЕ ДОСЬЕ", sTitle),
        Paragraph("Дело Бобова Олега Ивановича", sH1),
        Paragraph("Взыскание ущерба с ООО «УЖК Новоуральская»", sBody),
        Spacer(1, 1*cm),
        Paragraph("Дата сборки: 25.03.2026", sBody),
        PageBreak()
    ]

    for item in FILES:
        story.append(Paragraph(item["title"], sH1))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.lightgrey, spaceAfter=12))
        
        if os.path.exists(item["path"]):
            with open(item["path"], "r", encoding="utf-8") as f:
                content = f.read()
                # Simple markdown-to-pdf logic for lines
                for line in content.split("\n"):
                    if line.strip():
                        story.append(Paragraph(line, sBody))
        else:
            story.append(Paragraph(f"[ОШИБКА: Файл {item['title']} не найден]", sBody))
        
        story.append(PageBreak())

    doc.build(story)
    print(f"✅ PDF собран: {output_pdf}")

# ─── Сборка HTML ──────────────────────────────────────────────────────────────
def generate_html():
    output_html = os.path.join(OUTPUT_DIR, "index.html")
    
    html_content = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Юридическое Досье - Бобов О.И.</title>
        <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;700&display=swap" rel="stylesheet">
        <style>
            :root {
                --primary: #1a3c5e;
                --accent: #e8453c;
                --bg: #0f172a;
                --card-bg: rgba(30, 41, 59, 0.7);
                --text: #f1f5f9;
            }
            body {
                font-family: 'Montserrat', sans-serif;
                background: var(--bg);
                color: var(--text);
                margin: 0;
                display: flex;
                min-height: 100vh;
            }
            .sidebar {
                width: 250px;
                background: rgba(15, 23, 42, 0.9);
                border-right: 1px solid rgba(255,255,255,0.1);
                padding: 2rem;
                position: sticky;
                top: 0;
                height: 100vh;
            }
            .content {
                flex: 1;
                padding: 3rem;
                overflow-y: auto;
            }
            .sidebar h1 { font-size: 1.2rem; color: var(--accent); margin-bottom: 2rem; }
            .nav-item {
                display: block;
                padding: 0.8rem;
                color: #94a3b8;
                text-decoration: none;
                border-radius: 8px;
                transition: 0.3s;
                margin-bottom: 0.5rem;
            }
            .nav-item:hover, .nav-item.active {
                background: var(--primary);
                color: white;
            }
            .section {
                background: var(--card-bg);
                backdrop-filter: blur(10px);
                border-radius: 16px;
                padding: 2.5rem;
                margin-bottom: 3rem;
                border: 1px solid rgba(255,255,255,0.05);
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            }
            h2 { color: var(--accent); border-bottom: 1px solid rgba(232, 69, 60, 0.3); padding-bottom: 0.5rem; }
            pre { 
                white-space: pre-wrap; 
                background: rgba(0,0,0,0.2); 
                padding: 1.5rem; 
                border-radius: 8px; 
                font-family: inherit; 
                line-height: 1.6;
            }
            .btn-download {
                display: inline-block;
                padding: 1rem 2rem;
                background: var(--accent);
                color: white;
                text-decoration: none;
                border-radius: 50px;
                font-weight: bold;
                margin-top: 1rem;
                box-shadow: 0 4px 15px rgba(232, 69, 60, 0.4);
            }
        </style>
    </head>
    <body>
        <div class="sidebar">
            <h1>ДОСЬЕ: БОБОВ</h1>
            <nav>
                <a href="#report-father" class="nav-item active">Отчет для отца</a>
                <a href="#complaint" class="nav-item">Финальная жалоба</a>
                <a href="#arguments" class="nav-item">Правовая база</a>
                <a href="#instructions" class="nav-item">Инструкции</a>
                <a href="#inventory" class="nav-item">Опись (Шаблон)</a>
            </nav>
            <a href="legal_dossier_bobov.pdf" class="btn-download" download>Скачать PDF</a>
        </div>
        <div class="content">
    """

    for item in FILES:
        anchor_id = item["title"].lower().replace(" ", "-") # Simple slug
        if "ОТЧЕТ" in item["title"]: anchor_id = "report-father"
        elif "ЖАЛОБА" in item["title"]: anchor_id = "complaint"
        elif "АРГУМЕНТЫ" in item["title"]: anchor_id = "arguments"
        elif "ИНСТРУКЦИЯ" in item["title"]: anchor_id = "instructions"
        elif "ШАБЛОН" in item["title"]: anchor_id = "inventory"

        html_content += f'<div id="{anchor_id}" class="section"><h2>{item["title"]}</h2>'
        
        if os.path.exists(item["path"]):
            with open(item["path"], "r", encoding="utf-8") as f:
                raw_text = f.read()
                if item["type"] == "md":
                    # Simple markdown rendering with replacement for basic tags
                    rendered = raw_text.replace("# ", "<h3>").replace("### ", "<h4>").replace("\n", "<br>")
                    html_content += f'<div class="md-content">{rendered}</div>'
                else:
                    html_content += f"<pre>{raw_text}</pre>"
        else:
            html_content += "<p>Файл не найден.</p>"
        
        html_content += "</div>"

    html_content += """
        </div>
        <script>
            // Simple scroll spy logic
            const navItems = document.querySelectorAll('.nav-item');
            window.addEventListener('scroll', () => {
                let current = '';
                document.querySelectorAll('.section').forEach(section => {
                    const sectionTop = section.offsetTop;
                    if (pageYOffset >= sectionTop - 60) {
                        current = section.getAttribute('id');
                    }
                });
                navItems.forEach(item => {
                    item.classList.remove('active');
                    if (item.getAttribute('href').includes(current)) {
                        item.classList.add('active');
                    }
                });
            });
        </script>
    </body>
    </html>
    """
    
    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✅ HTML готов: {output_html}")

if __name__ == "__main__":
    generate_pdf()
    generate_html()
