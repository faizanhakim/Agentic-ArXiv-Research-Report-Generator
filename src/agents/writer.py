from src.prompts import WRITER_SYSTEM, WRITER_USER_TEMPLATE
from src.rag.index_builder import query_index
from llama_index.core import Settings  # ✅ use global LLM settings


def _snippets_for_prompt(retrieval_text: str) -> str:
    return retrieval_text


def write_report(index, topic: str) -> str:
    """
    Retrieves key snippets from the index and generates a structured research report.
    Uses the globally configured Settings.llm (no more service_context).
    """
    # retrieve relevant chunks
    snippets = query_index(index, f"Collect key research snippets about: {topic}", top_k=8)
    user_prompt = WRITER_USER_TEMPLATE.format(topic=topic, snippets=_snippets_for_prompt(snippets))

    # ✅ use globally configured LLM
    llm = Settings.llm
    prompt = WRITER_SYSTEM + "\n\n" + user_prompt
    response = llm.complete(prompt)

    report_text = response.text

    # ensure References section exists
    if "References" not in report_text:
        report_text += "\n\nReferences:\n- (No explicit citations found. Verify manually.)"
    return report_text
