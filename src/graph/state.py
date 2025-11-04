from typing import TypedDict, List, Dict, Optional
from llama_index.core import VectorStoreIndex

class GraphState(TypedDict, total=False):
    topic: str
    plan: str
    papers: List[Dict]
    index: VectorStoreIndex
    report: str
    reviewer_feedback: str
    score: float
    iterations: int
