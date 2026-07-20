"""
Batch test harness: runs a fixed set of hard-coded questions (1 PDF-scoped,
1 web-scoped) through the same crew in a single execution, so both
retrieval paths can be inspected without re-running the script per question.

The crew (and its RagTool index) is built once and reused via
Crew.kickoff_for_each(), which copies the crew per input internally rather
than rebuilding it from scratch — so the PDF is only embedded once, not
once per question.
"""

from pathlib import Path

from dotenv import load_dotenv

from crew import build_crew

load_dotenv()

PDF_PATH = Path(__file__).parent / "transformer_research_paper-dataset.pdf"

QUESTIONS = [
    # --- PDF-scoped: should route to 'pdf' ---
    "What is the attention mechanism described in the paper?",
    # --- Web-scoped: should route to 'web' ---
    "What is the latest news in AI this week?",
]


def main() -> None:
    crew = build_crew(PDF_PATH)

    results = crew.kickoff_for_each(inputs=[{"question": q} for q in QUESTIONS])

    print("\n\n" + "=" * 80)
    print("BATCH RESULTS")
    print("=" * 80)
    for question, result in zip(QUESTIONS, results):
        routing_decision = result.tasks_output[0].raw  # Router task runs first
        print(f"\n--- Question: {question} ---")
        print(f"Routing decision: {routing_decision}")
        print(f"\nAnswer:\n{result.raw}")
        print("-" * 80)


if __name__ == "__main__":
    main()
