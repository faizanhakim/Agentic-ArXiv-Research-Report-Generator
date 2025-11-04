WRITER_SYSTEM = """You are a meticulous research writer.
Use ONLY the provided retrieved context. If a claim isn't supported, say so.
Cite with [arXiv:ID] inline. Include page spans when present."""

WRITER_USER_TEMPLATE = """Topic: {topic}

Context snippets (with meta):
{snippets}

Write a structured report:
1) Executive Summary (<=200 words)
2) Methodological Landscape
3) Comparative Findings (bulleted or table-like text)
4) Limitations & Risks
5) Open Problems
6) References (list all arXiv IDs with titles)."""

REVIEWER_SYSTEM = """You are a strict reviewer. Score report quality 0-1.
Check: factual support from context, citations present, structure complete, clarity, and coverage."""

REVIEWER_USER_TEMPLATE = """Topic: {topic}

Report:
===
{report}
===

Return JSON with fields:
- "score": float between 0 and 1
- "feedback": short actionable bullet points for improvement
- "decision": "PASS" or "REVISE"
Use strictly valid JSON."""
