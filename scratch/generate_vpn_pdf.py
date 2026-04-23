import os
import urllib.request
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FONT_DIR = os.path.join(os.path.dirname(__file__), "..", "fonts")

def register_fonts():
    os.makedirs(FONT_DIR, exist_ok=True)
    FONTS = {
        "DejaVu":       "https://cdn.jsdelivr.net/npm/dejavu-fonts-ttf@2.37.3/ttf/DejaVuSans.ttf",
        "DejaVu-Bold":  "https://cdn.jsdelivr.net/npm/dejavu-fonts-ttf@2.37.3/ttf/DejaVuSans-Bold.ttf",
    }
    for name, url in FONTS.items():
        path = os.path.join(FONT_DIR, f"{name}.ttf")
        if not os.path.exists(path):
            print(f"Скачиваю шрифт {name}...")
            urllib.request.urlretrieve(url, path)
        pdfmetrics.registerFont(TTFont(name, path))

register_fonts()

def S(name, **kw):
    kw.setdefault("fontName", "DejaVu")
    return ParagraphStyle(name, **kw)

sTitle = S("sTitle", fontName="DejaVu-Bold", fontSize=18, leading=22, textColor=colors.HexColor("#0033A0"), spaceAfter=10)
sH1 = S("sH1", fontName="DejaVu-Bold", fontSize=14, leading=18, textColor=colors.HexColor("#009EDB"), spaceBefore=15, spaceAfter=8)
sBody = S("sBody", fontSize=11, leading=16, spaceAfter=8)
sCode = S("sCode", fontName="DejaVu", fontSize=9, leading=13, backColor=colors.HexColor("#f1f5f9"), textColor=colors.HexColor("#334155"), leftIndent=10, rightIndent=10, borderPadding=(5, 5, 5, 5), spaceAfter=8)

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "..", "obsidian_brain", "vpn_troubleshooting.pdf")

doc = SimpleDocTemplate(OUTPUT_FILE, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
story = []

story.append(Paragraph("Восстановление работы VPN (AirLink / Tun)", sTitle))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#009EDB"), spaceAfter=15))

story.append(Paragraph("Описание проблемы", sH1))
story.append(Paragraph("VPN-клиенты (особенно использующие tun-интерфейсы) могут перестать работать и выдавать ошибки таймаута (например, i/o timeout).", sBody))
story.append(Paragraph("Чаще всего это происходит, если в Windows были глобально заданы прокси-переменные или включен системный прокси. Возникает «мертвая петля» (routing loop).", sBody))

story.append(Paragraph("Как проверить наличие проблемы", sH1))
story.append(Paragraph("В PowerShell (без прав администратора):", sBody))
story.append(Paragraph("1. Проверка переменных:", sBody))
story.append(Paragraph("Get-ChildItem Env: | Where-Object Name -match 'proxy'", sCode))
story.append(Paragraph("2. Проверка системного прокси:", sBody))
story.append(Paragraph("Get-ItemProperty -Path 'Registry::HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings' | Select-Object ProxyEnable, ProxyServer", sCode))

story.append(Paragraph("Решение (Скрипт очистки)", sH1))
story.append(Paragraph("Скопируйте и выполните этот скрипт в PowerShell. Он удалит конфликтующие переменные и выключит системный прокси:", sBody))
story.append(Paragraph("[System.Environment]::SetEnvironmentVariable('HTTP_PROXY', $null, 'User')<br/>[System.Environment]::SetEnvironmentVariable('HTTPS_PROXY', $null, 'User')<br/>[System.Environment]::SetEnvironmentVariable('HTTP_PROXY', $null, 'Machine')<br/>[System.Environment]::SetEnvironmentVariable('HTTPS_PROXY', $null, 'Machine')<br/>Set-ItemProperty -Path 'Registry::HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings' -Name ProxyEnable -Value 0", sCode))

story.append(Paragraph("Последующие шаги", sH1))
story.append(Paragraph("После выполнения скрипта обязательно перезагрузите компьютер. Запустите VPN-клиент заново — соединение должно восстановиться.", sBody))

doc.build(story)
print(f"PDF успешно создан: {OUTPUT_FILE}")
