"""
Local CLI entry point for the agentic RAG crew. See crew.py for the
Router/Retriever agent definitions — this file just wires up local
concerns (loading .env, resolving the PDF path, reading CLI args).
"""

import sys
from pathlib import Path

from dotenv import load_dotenv

from crew import build_crew

load_dotenv()

PDF_PATH = Path(__file__).parent / "transformer_research_paper-dataset.pdf"


def main() -> None:
    question = " ".join(sys.argv[1:]).strip()
    if not question:
        question = input("Enter your question: ").strip()

    crew = build_crew(PDF_PATH)
    result = crew.kickoff(inputs={"question": question})

    routing_decision = result.tasks_output[0].raw  # Router task runs first
    print(f"\n=== Routing Decision ===\n{routing_decision}")
    print(f"\n=== Final Answer ===\n{result.raw}")


if __name__ == "__main__":
    main()
