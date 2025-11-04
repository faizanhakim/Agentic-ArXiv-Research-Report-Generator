# arxiv-agent (LangGraph + LlamaIndex + Ollama)

Agentic pipeline that:
1) Searches arXiv
2) Downloads PDFs
3) Builds a RAG index with LlamaIndex (Ollama embeddings)
4) Generates a structured, cited report
5) Runs a Reviewer loop for quality

## Setup

```bash
pip install -r requirements.txt
cp .env.sample .env
# ensure ollama is running and models are pulled
ollama pull llama3
