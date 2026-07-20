"""
Shared crew-building logic for the agentic RAG system, with two role-based
agents:

- Router Agent: classifies the incoming question as answerable from the
  indexed PDF ("pdf") or requiring a live web search ("web").
- Retriever Agent: executes retrieval using the tool matching the routing
  decision (RagTool for the PDF, TavilySearchTool for the web) and
  formulates a source-grounded final answer.

This module has no environment-specific assumptions (no hardcoded local
paths, no CLI parsing) so it can be imported identically from main.py
(local CLI) or a Colab notebook.
"""

from pathlib import Path
from typing import Union

from crewai import Agent, Task, Crew, Process
from crewai_tools import RagTool, TavilySearchTool

LLM_MODEL = "gpt-4o-mini"


def build_crew(pdf_path: Union[str, Path]) -> Crew:
    """Build the Router + Retriever crew, indexed against the given PDF."""

    # --- Tools ---
    rag_tool = RagTool()  # out-of-the-box config: ChromaDB + OpenAI embeddings
    rag_tool.add(data_type="pdf_file", path=str(pdf_path))

    web_search_tool = TavilySearchTool(search_depth="basic", max_results=5)

    # --- Agents ---
    router = Agent(
        role="Query Router",
        goal=(
            "Classify each incoming question as either 'pdf' or 'web'. "
            "Choose 'pdf' if the question is about the Transformer research "
            "paper's content (architecture, attention mechanism, training "
            "details, results, etc.) — anything likely covered in an "
            "academic paper on Transformers. Choose 'web' if the question "
            "asks about current events, recent news, or anything outside "
            "the scope of that paper."
        ),
        backstory=(
            "An expert at understanding what a question is really asking "
            "and routing it to the retrieval method most likely to answer "
            "it accurately."
        ),
        llm=LLM_MODEL,
        verbose=True,
    )

    retriever = Agent(
        role="Retriever",
        goal=(
            "Retrieve accurate, source-grounded information using the "
            "correct tool as directed by the routing decision, then "
            "compose a clear final answer that cites where the information "
            "came from."
        ),
        backstory=(
            "A meticulous researcher who only uses the retrieval method "
            "assigned to them and never fabricates information not found "
            "in the retrieved source."
        ),
        tools=[rag_tool, web_search_tool],
        llm=LLM_MODEL,
        verbose=True,
    )

    # --- Tasks ---
    route_task = Task(
        description=(
            "Question: {question}\n\n"
            "Decide whether this question should be answered using the "
            "PDF knowledge base ('pdf') or a live web search ('web'). "
            "Respond with exactly one word — 'pdf' or 'web' — followed by "
            "a one-sentence justification."
        ),
        expected_output="One word ('pdf' or 'web') plus a one-sentence justification.",
        agent=router,
    )

    retrieve_task = Task(
        description=(
            "Original question: {question}\n\n"
            "The routing decision above tells you which tool to use. "
            "If the decision was 'pdf', use ONLY the PDF knowledge base "
            "tool. If it was 'web', use ONLY the web search tool. Do not "
            "use both. Retrieve the relevant information and answer the "
            "original question clearly and accurately, citing the source "
            "(the paper, or the web result URL) you used."
        ),
        expected_output=(
            "A clear, accurate answer to the original question, with a "
            "citation of the source used (paper section, or web URL)."
        ),
        agent=retriever,
        context=[route_task],
    )

    return Crew(
        agents=[router, retriever],
        tasks=[route_task, retrieve_task],
        process=Process.sequential,
        verbose=True,
    )
