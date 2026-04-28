import fitz  # PyMuPDF
import os

def extract_text(pdf_path, txt_path):
    if not os.path.exists(pdf_path):
        print(f"File not found: {pdf_path}")
        return
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Success: {txt_path}")

# Ищем файл сверления по маске в rosatom_attachments
import glob
files = glob.glob("C:/ANTIGRAVITY/1/rosatom_attachments/10.129.0.04*")
if files:
    extract_text(files[0], "C:/ANTIGRAVITY/1/scratch/device_drilling.txt")
else:
    print("Drilling device PDF not found.")
