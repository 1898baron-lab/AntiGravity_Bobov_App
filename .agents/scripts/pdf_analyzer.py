"""
PDF Analyzer for Engineering Drawings
Converts PDF pages to PNG images and extracts text.
Usage: python pdf_analyzer.py <path_to_pdf> [output_dir]
"""
import sys
import os

try:
    import fitz  # PyMuPDF
except ImportError:
    # Try the full path Python
    print("ERROR: PyMuPDF not found. Run: pip install PyMuPDF")
    sys.exit(1)


def analyze_pdf(pdf_path, output_dir=None):
    if not os.path.exists(pdf_path):
        print(f"ERROR: File not found: {pdf_path}")
        return

    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(pdf_path), "_pdf_export")
    os.makedirs(output_dir, exist_ok=True)

    doc = fitz.open(pdf_path)
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]

    print(f"File: {pdf_path}")
    print(f"Pages: {len(doc)}")
    print(f"Output: {output_dir}")
    print("-" * 60)

    for page_num in range(len(doc)):
        page = doc[page_num]

        # Extract text
        text = page.get_text("text")
        if text.strip():
            print(f"\n--- Page {page_num + 1} TEXT ---")
            print(text[:2000])  # First 2000 chars

        # Render page to PNG (300 DPI for engineering drawings)
        mat = fitz.Matrix(300 / 72, 300 / 72)
        pix = page.get_pixmap(matrix=mat)
        img_path = os.path.join(output_dir, f"{base_name}_page_{page_num + 1}.png")
        pix.save(img_path)
        print(f"Saved: {img_path} ({pix.width}x{pix.height})")

    doc.close()
    print(f"\nDone. {len(doc)} pages exported to {output_dir}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pdf_analyzer.py <pdf_path> [output_dir]")
        sys.exit(1)

    pdf_file = sys.argv[1]
    out_dir = sys.argv[2] if len(sys.argv) > 2 else None
    analyze_pdf(pdf_file, out_dir)
