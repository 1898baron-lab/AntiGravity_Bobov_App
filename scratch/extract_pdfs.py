import fitz  # PyMuPDF
import json

def extract_text(pdf_path, txt_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)
    return text

files = [
    ("C:/ANTIGRAVITY/1/valve_dn170.pdf", "C:/ANTIGRAVITY/1/scratch/valve_dn170.txt"),
    ("C:/ANTIGRAVITY/1/scratch/main_tz.pdf", "C:/ANTIGRAVITY/1/scratch/main_tz.txt"),
    ("C:/ANTIGRAVITY/1/assembly_zeus.pdf", "C:/ANTIGRAVITY/1/scratch/assembly_zeus.txt")
]

for pdf, txt in files:
    try:
        print(f"Extracting {pdf}...")
        extract_text(pdf, txt)
        print(f"Success!")
    except Exception as e:
        print(f"Error {pdf}: {e}")
