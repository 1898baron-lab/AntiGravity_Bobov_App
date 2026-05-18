from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

def generate_legal_dossier():
    output_path = r'C:/ANTIGRAVITY/1/obsidian_brain/1_PROJECTS/BOBOV/BOBOV_LEGAL_DOSSIER_2026.pdf'
    source_file = r'C:/ANTIGRAVITY/1/obsidian_brain/1_PROJECTS/BOBOV/LEGAL_ATTACK_DRAFT_125.md'
    
    # Регистрация шрифта с поддержкой кириллицы (используем системный Arial)
    font_path = "C:/Windows/Fonts/arial.ttf"
    pdfmetrics.registerFont(TTFont('Arial', font_path))

    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    # Заголовок
    c.setFont('Arial', 16)
    c.drawCentredString(width/2, height - 50, "ЮРИДИЧЕСКОЕ ДОСЬЕ: ДЕЛО БОБОВА")
    c.setFont('Arial', 12)
    c.drawCentredString(width/2, height - 70, "Статус: LEGAL ATTACK (СТ. 125 УПК РФ)")
    
    c.line(50, height - 80, width - 50, height - 80)

    # Содержимое
    if os.path.exists(source_file):
        with open(source_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        y = height - 110
        c.setFont('Arial', 10)
        for line in lines:
            if y < 50:
                c.showPage()
                c.setFont('Arial', 10)
                y = height - 50
            
            clean_line = line.strip().replace('**', '').replace('#', '')
            c.drawString(50, y, clean_line)
            y -= 15
    else:
        c.drawString(50, height - 110, "ОШИБКА: Файл черновика не найден.")

    c.save()
    print(f"Досье успешно создано: {output_path}")

if __name__ == "__main__":
    generate_legal_dossier()
