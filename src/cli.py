import argparse
import os
from datetime import datetime
from src.logging_config import setup_logging
from src.config import OUTPUT_DIR
from src.graph.app import build_app

def main():
    parser = argparse.ArgumentParser(description="Agentic arXiv report generator")
    parser.add_argument("--topic", required=True, type=str)
    parser.add_argument("--max-results", type=int, default=6)
    parser.add_argument("--out", type=str, default=None)
    args = parser.parse_args()

    logger = setup_logging()

    app = build_app()
    state = {
        "topic": args.topic,
        "max_results": args.max_results,
        "iterations": 0
    }
    final = app.invoke(state)

    report = final.get("report", "(no report)")
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = args.out or os.path.join(OUTPUT_DIR, f"report_{ts}.md")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"# Literature Report: {args.topic}\n\n")
        f.write(report)
        f.write("\n")

    print(f"\n✅ Saved report to: {out_path}")

if __name__ == "__main__":
    main()
