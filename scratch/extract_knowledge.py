import docx
import os
import PyPDF2

def extract_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_pdf(file_path):
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

base_path = r"c:\ANTIGRAVITY\1\research\chatgpt_imports"
files = [
    "Программа стажировки Бобов К.О.docx",
    "ЗАКРЕП v1.0.docx",
    "План освоения новой профессии_ инженер-конструктор оснастки.docx",
    "Отчёт по анализу ответов ИИ в области машиностроения.pdf"
]

for file in files:
    full_path = os.path.join(base_path, file)
    print(f"--- EXTRACTING: {file} ---")
    try:
        if file.endswith(".docx"):
            print(extract_docx(full_path))
        elif file.endswith(".pdf"):
            print(extract_pdf(full_path))
    except Exception as e:
        print(f"Error reading {file}: {e}")
    print("\n" + "="*50 + "\n")
