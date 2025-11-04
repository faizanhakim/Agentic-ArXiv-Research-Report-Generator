from typing import Dict
import fitz

def extract_text_with_pages(pdf_path: str) -> Dict[int, str]:
    """
    Returns a mapping {page_number: text}
    """
    doc = fitz.open(pdf_path)
    pages = {}
    for i, page in enumerate(doc):
        pages[i + 1] = page.get_text("text")
    return pages
