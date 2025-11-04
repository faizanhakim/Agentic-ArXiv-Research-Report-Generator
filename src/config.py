import os
from dotenv import load_dotenv

load_dotenv()

def _get(name: str, default: str) -> str:
    return os.getenv(name, default)

OLLAMA_LLM = _get("OLLAMA_LLM", "llama3")
OLLAMA_EMBED = _get("OLLAMA_EMBED", OLLAMA_LLM)

DATA_DIR = _get("DATA_DIR", "./data")
PDF_DIR = _get("PDF_DIR", os.path.join(DATA_DIR, "pdfs"))
OUTPUT_DIR = _get("OUTPUT_DIR", os.path.join(DATA_DIR, "outputs"))

CHUNK_SIZE = int(_get("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(_get("CHUNK_OVERLAP", "120"))

TOP_K = int(_get("TOP_K", "6"))

MAX_REWRITES = int(_get("MAX_REWRITES", "1"))
QUALITY_THRESHOLD = float(_get("QUALITY_THRESHOLD", "0.65"))

os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
