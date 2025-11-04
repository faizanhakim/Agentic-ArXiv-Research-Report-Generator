from typing import Dict

def plan(topic: str) -> Dict:
    """
    Minimal planner: in real systems you'd expand into sub-questions.
    """
    return {"plan": f"Search arXiv for: {topic}. Index results. Generate report with citations."}
