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

output_file = os.path.join(base_path, "extracted_knowledge_summary.md")
with open(output_file, 'w', encoding='utf-8') as out:
    for file in files:
        full_path = os.path.join(base_path, file)
        out.write(f"# EXTRACTING: {file}\n\n")
        try:
            content = ""
            if file.endswith(".docx"):
                content = extract_docx(full_path)
            elif file.endswith(".pdf"):
                content = extract_pdf(full_path)
            out.write(content + "\n\n")
            out.write("="*50 + "\n\n")
        except Exception as e:
            out.write(f"Error reading {file}: {e}\n\n")
