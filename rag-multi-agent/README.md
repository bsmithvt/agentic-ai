# Agentic RAG — Multi-Agent Router + Retriever

A multi-agent Retrieval-Augmented Generation system that answers questions using either a PDF knowledge base or a live web search, chosen automatically per question. Built with CrewAI, RagTool (ChromaDB + OpenAI embeddings), and Tavily.

## How It Works

1. **Route** — A Router Agent classifies each incoming question as either `pdf` (answerable from the indexed research paper) or `web` (needs current/external information)
2. **Retrieve** — A Retriever Agent executes retrieval using the tool matching that classification:
   - `pdf` → CrewAI's `RagTool`, which chunks, embeds, and indexes the PDF into a local ChromaDB vector store, then performs similarity search
   - `web` → `TavilySearchTool`, which performs a live web search
3. **Answer** — The Retriever Agent composes a final answer from the retrieved content, citing the source used (paper section or web URL)

The two agents run sequentially via CrewAI's `Process.sequential` — the Router's classification is passed as context into the Retriever's task.

## Project Files

| File | Description |
|---|---|
| `crew.py` | Shared crew-building logic — defines the Router Agent, Retriever Agent, tasks, and tools. Imported by both `main.py` and the Colab notebook. |
| `main.py` | Local CLI entry point — loads `.env`, resolves the PDF path, and runs the crew against a single question (CLI arg or interactive prompt) |
| `run_batch.py` | Runs a fixed set of hard-coded questions (one PDF-scoped, one web-scoped) through the same crew in a single execution, so both retrieval paths can be inspected together |
| `colab_notebook.ipynb` | Google Colab-compatible notebook version — install, upload, set API keys via Colab Secrets, and run |
| `install.sh` | Shell script to create the venv (Python 3.12 specifically) and install pinned dependencies |
| `requirements.txt` | Python package list (pinned to the versions this was built and tested against) |
| `transformer_research_paper-dataset.pdf` | Source document indexed for the PDF retrieval path |
| `OUTPUT.md` | Full sample output (reasoning-trace visualization + final answers) from a real `run_batch.py` execution |
| `.env` | Local API keys — **not committed to git.** You must supply your own (see Setup below); this repo does not include working keys. |

## Requirements

- **Python 3.12 specifically** — newer versions (3.13+, especially 3.14) can lack prebuilt wheels for some dependencies here, notably `tiktoken`, which then needs a Rust toolchain to build from source and will fail without one. `install.sh` checks for `python3.12` on `PATH` and exits with an install hint if it's missing, rather than silently falling back to a different Python version.
- An **OpenAI API key** (get one at [platform.openai.com](https://platform.openai.com)) — used for the agents' reasoning LLM (`gpt-4o-mini`) and for RagTool's default embeddings
- A **Tavily API key** (get one at [tavily.com](https://tavily.com), free tier available) — used for the web search path

> **Note for graders/reviewers:** this repo intentionally does not include a `.env` file or working API keys. To run this locally, you'll need to create your own `.env` with your own `OPENAI_API_KEY` and `TAVILY_API_KEY` (see step 2 below) — without them, the crew will fail on the first LLM/tool call regardless of whether installation succeeds.

## Setup

### 1. Install dependencies

```bash
bash install.sh
```

This creates a `.venv` using `python3.12` and installs the pinned dependencies from `requirements.txt`. If `python3.12` isn't found, it exits with an install hint (e.g. `brew install python@3.12` on macOS) instead of falling back to whatever `python3` happens to resolve to.

**Or manually:**
```bash
python3.12 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

### 2. Set your API keys

Create a `.env` file in this directory:

```bash
OPENAI_API_KEY=sk-...
TAVILY_API_KEY=tvly-...
```

## Running the Pipeline

**Locally:**
```bash
.venv/bin/python main.py "What is the attention mechanism described in the paper?"
```

Or run with no argument to be prompted interactively:
```bash
.venv/bin/python main.py
```

**Google Colab:**
Upload `colab_notebook.ipynb` to [colab.research.google.com](https://colab.research.google.com) and run the cells in order. You'll be prompted to upload `crew.py` and the PDF, and to provide API keys (via Colab Secrets or manual entry).

On first run, `RagTool` will chunk and embed the full PDF via the OpenAI Embeddings API and build a local ChromaDB store — this takes a little time and a small amount of embedding-token cost. Subsequent runs reuse the same in-memory index for the life of the process.

## Sample Output

See [OUTPUT.md](./OUTPUT.md) for a full sample run — the complete reasoning-trace visualization (agent starts, tool calls, final answers) plus the routing-decision/answer summary, captured from a real local execution of `run_batch.py` covering one PDF-scoped question and one web-scoped question.

## Models Used

| Model | Purpose | When Called |
|---|---|---|
| `gpt-4o-mini` | Router Agent's classification reasoning | Each query |
| `gpt-4o-mini` | Retriever Agent's retrieval + answer synthesis | Each query |
| OpenAI default embedding model | Convert PDF chunks to vectors for RagTool | PDF index build (first `RagTool.add()` call) |
