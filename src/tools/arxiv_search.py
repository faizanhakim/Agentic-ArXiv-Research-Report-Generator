from typing import List, Dict
import os, requests, arxiv, logging
from tqdm import tqdm
from src.config import PDF_DIR

log = logging.getLogger(__name__)

def fetch_arxiv_papers(query: str, max_results: int = 5) -> List[Dict]:
    """
    Search arXiv, download PDFs if missing, and return metadata.
    """
    os.makedirs(PDF_DIR, exist_ok=True)
    results: List[Dict] = []
    search = arxiv.Search(query=query, max_results=max_results, sort_by=arxiv.SortCriterion.Relevance)
    log.info("Searching arXiv for: %s", query)
    for r in tqdm(search.results(), desc="Downloading PDFs"):
        short_id = r.get_short_id()
        pdf_path = os.path.join(PDF_DIR, f"{short_id}.pdf")
        if not os.path.exists(pdf_path):
            resp = requests.get(r.pdf_url, timeout=60)
            resp.raise_for_status()
            with open(pdf_path, "wb") as f:
                f.write(resp.content)
        results.append({
            "id": short_id,
            "title": r.title,
            "authors": [a.name for a in r.authors],
            "year": r.published.year if r.published else None,
            "pdf_path": pdf_path,
            "summary": r.summary
        })
    log.info("Fetched %d papers", len(results))
    return results
