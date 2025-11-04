import logging
from typing import Dict
from src.agents.planner import plan
from src.tools.arxiv_search import fetch_arxiv_papers
from src.rag.index_builder import build_index_from_metadata
from src.agents.writer import write_report
from src.agents.reviewer import review_report
from src.config import MAX_REWRITES, QUALITY_THRESHOLD

log = logging.getLogger(__name__)

def planner_node(state: Dict) -> Dict:
    topic = state["topic"]
    p = plan(topic)
    log.info("Plan: %s", p["plan"])
    return {"plan": p["plan"]}

def search_node(state: Dict) -> Dict:
    topic = state["topic"]
    papers = fetch_arxiv_papers(topic, max_results=state.get("max_results", 5))
    return {"papers": papers}

def index_node(state: Dict) -> Dict:
    index = build_index_from_metadata(state["papers"])
    return {"index": index}

def writer_node(state: Dict) -> Dict:
    report = write_report(state["index"], state["topic"])
    return {"report": report}

def reviewer_node(state: Dict) -> Dict:
    score, feedback, decision = review_report(state["index"], state["topic"], state["report"])
    log.info("Review score=%.2f decision=%s", score, decision)
    return {"score": score, "reviewer_feedback": feedback, "decision": decision}

def decision_edge(state: Dict) -> str:
    # Decide whether to REWRITE or FINISH
    iterations = int(state.get("iterations", 0))
    score = float(state.get("score", 0.0))
    if score >= QUALITY_THRESHOLD:
        return "finish"
    if iterations >= MAX_REWRITES:
        return "finish"  # give up further rewrites
    return "rewrite"

def rewrite_node(state: Dict) -> Dict:
    """
    Ask the writer to improve based on reviewer feedback.
    """
    feedback = state.get("reviewer_feedback", "")
    topic = state["topic"]
    improved_prompt = f"{topic}\n\nIncorporate this feedback and improve:\n{feedback}"
    improved_report = write_report(state["index"], improved_prompt)
    return {"report": improved_report, "iterations": int(state.get("iterations", 0)) + 1}
