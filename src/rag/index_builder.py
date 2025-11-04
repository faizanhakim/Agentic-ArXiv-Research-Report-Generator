import logging
from typing import List, Dict
from llama_index.core import VectorStoreIndex, Document, Settings
from llama_index.llms.ollama import Ollama as LlamaOllama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core.node_parser import SentenceSplitter
from src.tools.pdf_utils import extract_text_with_pages
from src.config import OLLAMA_LLM, OLLAMA_EMBED, CHUNK_SIZE, CHUNK_OVERLAP, TOP_K

log = logging.getLogger(__name__)

# 🧠 Setup once at import time
llm = LlamaOllama(model=OLLAMA_LLM, request_timeout=180)
embed = OllamaEmbedding(model_name=OLLAMA_EMBED)

# Register in global Settings
Settings.llm = llm
Settings.embed_model = embed


def build_index_from_metadata(papers: List[Dict]) -> VectorStoreIndex:
    """
    Builds a VectorStoreIndex from list of papers.
    """
    documents: List[Document] = []
    splitter = SentenceSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)

    for p in papers:
        pages = extract_text_with_pages(p["pdf_path"])
        full_text = "\n".join(pages.values())
        doc = Document(
            text=full_text,
            metadata={
                "title": p["title"],
                "arxiv_id": p["id"],
                "year": p.get("year"),
            }
        )
        documents.append(doc)

    nodes = splitter.get_nodes_from_documents(documents)
    for n in nodes:
        meta = n.metadata or {}
        n.metadata = {
            "title": meta.get("title"),
            "arxiv_id": meta.get("arxiv_id"),
            "year": meta.get("year"),
        }

    index = VectorStoreIndex(nodes)
    log.info("Index built with %d nodes", len(nodes))
    return index


def query_index(index: VectorStoreIndex, prompt: str, top_k: int = TOP_K) -> str:
    qe = index.as_query_engine(similarity_top_k=top_k)
    resp = qe.query(prompt)
    return resp.response
