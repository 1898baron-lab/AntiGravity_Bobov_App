import os
import re
import urllib.request
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, PageBreak
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ─── Константы ────────────────────────────────────────────────────────────────
BASE_DIR = r"C:\ANTIGRAVITY\1"
REPORT_PATH = r"C:\Users\Sasha  Baron\.gemini\antigravity\brain\199232ee-e613-40c0-a5d3-faafc37dfb97\stolen_property_report.md"
OUTPUT_DIR = os.path.join(BASE_DIR, "legal_dossier_output")
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "Stolen_Property_Report.pdf")

# ─── Шрифты (DejaVu для кириллицы) ───────────────────────────────────────────
FONT_DIR = os.path.join(BASE_DIR, "scripts", "fonts")
os.makedirs(FONT_DIR, exist_ok=True)

FONTS = {
    "DejaVu":       "https://cdn.jsdelivr.net/npm/dejavu-fonts-ttf@2.37.3/ttf/DejaVuSans.ttf",
    "DejaVu-Bold":  "https://cdn.jsdelivr.net/npm/dejavu-fonts-ttf@2.37.3/ttf/DejaVuSans-Bold.ttf",
}

for name, url in FONTS.items():
    font_path = os.path.join(FONT_DIR, f"{name}.ttf")
    if not os.path.exists(font_path):
        print(f"Скачиваю шрифт {name}...")
        urllib.request.urlretrieve(url, font_path)
    pdfmetrics.registerFont(TTFont(name, font_path))

def md_to_html(text):
    # Заменяем **текст** на <b>текст</b>
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    # Заменяем [link](url) на link (упрощенно)
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
    return text

# ─── Сборка PDF ───────────────────────────────────────────────────────────────
def assemble_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_FILE, 
        pagesize=A4, 
        leftMargin=2*cm, rightMargin=2*cm, 
        topMargin=2*cm, bottomMargin=2*cm,
        title="Заявление о хищении имущества",
        author="AntiGravity Legal Assistant"
    )
    
    styles = getSampleStyleSheet()
    sTitle = ParagraphStyle("sTitle", fontName="DejaVu-Bold", fontSize=20, alignment=1, spaceAfter=20, textColor=colors.HexColor("#1A3C5E"))
    sH1 = ParagraphStyle("sH1", fontName="DejaVu-Bold", fontSize=14, spaceAfter=10, textColor=colors.HexColor("#1A3C5E"), spaceBefore=15)
    sBody = ParagraphStyle("sBody", fontName="DejaVu", fontSize=11, leading=14, spaceAfter=8)
    sTip = ParagraphStyle("sTip", fontName="DejaVu", fontSize=10, leading=12, textColor=colors.gray, leftIndent=0.5*cm)

    story = []

    # Читаем текст отчета
    if not os.path.exists(REPORT_PATH):
        print(f"Ошибка: Файл {REPORT_PATH} не найден")
        return

    with open(REPORT_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line:
            story.append(Spacer(1, 0.2*cm))
            continue
            
        if line.startswith("# "):
            story.append(Paragraph(md_to_html(line[2:]), sTitle))
            story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1A3C5E"), spaceAfter=12))
        elif line.startswith("## "):
            story.append(Paragraph(md_to_html(line[3:]), sH1))
        elif line.startswith("### "):
            story.append(Paragraph(md_to_html(line[4:]), sH1))
        elif line.startswith("> [!IMPORTANT]") or line.startswith("> [!TIP]"):
            continue 
        elif line.startswith("> "):
            story.append(Paragraph(md_to_html(line[2:]), sTip))
        elif line.startswith("---"):
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey, spaceAfter=10, spaceBefore=10))
        elif line.startswith("- ") or line.startswith("* "):
            story.append(Paragraph("• " + md_to_html(line[2:]), sBody))
        else:
            story.append(Paragraph(md_to_html(line), sBody))

    doc.build(story)
    print(f"✅ PDF успешно создан: {OUTPUT_FILE}")

if __name__ == "__main__":
    assemble_pdf()
