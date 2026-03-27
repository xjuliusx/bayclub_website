#!/usr/bin/env python3
import sys
import os
from pathlib import Path

# Requires: pip install pymupdf
try:
    import fitz  # PyMuPDF
except Exception as e:
    print("ERROR: PyMuPDF (pymupdf) not installed. Install with: pip install pymupdf", file=sys.stderr)
    sys.exit(2)

def generate(pdf_path: Path, out_dir: Path, scale: float = 2.0):
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    out_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(pdf_path)
    images = []
    for page_index in range(len(doc)):
        page = doc.load_page(page_index)
        mat = fitz.Matrix(scale, scale)  # zoom for higher-res thumbnail
        pix = page.get_pixmap(matrix=mat, alpha=False)
        out_file = out_dir / f"{pdf_path.stem.replace(' ', '_').lower()}_p{page_index+1}.png"
        pix.save(out_file.as_posix())
        images.append(out_file)
    return images

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: generate_pdf_thumbnails.py <input.pdf> <output_dir> [scale]", file=sys.stderr)
        sys.exit(1)
    pdf = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    scale = float(sys.argv[3]) if len(sys.argv) > 3 else 2.0
    out_files = generate(pdf, out_dir, scale)
    for f in out_files:
        print(f)
