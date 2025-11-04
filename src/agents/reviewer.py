import json
from llama_index.core import Settings
from src.prompts import REVIEWER_SYSTEM, REVIEWER_USER_TEMPLATE

def review_report(index, topic: str, report: str):
    """
    Returns (score, feedback, decision) from the reviewer model.
    Uses globally configured Settings.llm.
    """
    llm = Settings.llm 

    user_prompt = REVIEWER_USER_TEMPLATE.format(topic=topic, report=report)
    full_prompt = REVIEWER_SYSTEM + "\n\n" + user_prompt

    # Run the LLM
    completion = llm.complete(full_prompt)
    raw_text = completion.text.strip()

    # Parse JSON safely
    try:
        data = json.loads(raw_text)
        score = float(data.get("score", 0))
        feedback = data.get("feedback", "")
        decision = data.get("decision", "REVISE").upper()
    except Exception as e:
        score, feedback, decision = 0.0, f"Invalid JSON from reviewer: {e}\nRaw: {raw_text}", "REVISE"

    return score, feedback, decision
