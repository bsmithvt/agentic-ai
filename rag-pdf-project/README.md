# RAG Pipeline — PDF Chunking and Retrieval

An AI-powered document assistant that answers questions by retrieving relevant content from a set of PDF documents. Built with LangChain, FAISS, and OpenAI.

## How It Works

1. **Load** — PDF documents are loaded and parsed page by page
2. **Chunk** — Pages are split into 500-character overlapping text chunks
3. **Embed** — Each chunk is converted into a vector using OpenAI's `text-embedding-3-small` model
4. **Index** — Vectors are stored in a local FAISS index saved to `faiss_index/`
5. **Query** — A user question is embedded and compared against the index; the top 3 matching chunks are retrieved and passed to `gpt-4o-mini` to generate an answer

See `architecture_diagram.txt` for a full visual of the pipeline.

## Project Files

| File | Description |
|---|---|
| `rag_pipeline.py` | Main pipeline — load, chunk, embed, index, and query |
| `generate_pdfs.py` | Generates the 3 sample PDF documents |
| `install.sh` | Shell script to install all dependencies |
| `requirements.txt` | Python package list |
| `colab_install.py` | Dependency installer for Google Colab |
| `architecture_diagram.txt` | ASCII diagram of the pipeline and OpenAI API calls |
| `network_security_manual.pdf` | Sample document — network security topics |
| `climate_change_report.pdf` | Sample document — climate change report |
| `ml_fundamentals_guide.pdf` | Sample document — machine learning fundamentals |
| `faiss_index/` | Saved FAISS vector index (generated on first run) |

## Requirements

- Python 3.9+
- An OpenAI API key (get one at [platform.openai.com](https://platform.openai.com))
- The key must have **Model capabilities** and **Embeddings** scopes enabled

## Setup

### 1. Install dependencies

**Mac / Linux:**
```bash
bash install.sh
```

**Google Colab:**
```python
exec(open("colab_install.py").read())
```

**Or manually:**
```bash
pip install -r requirements.txt
```

### 2. (Optional) Set your OpenAI API key as an environment variable

```bash
export OPENAI_API_KEY="sk-..."
```

If this is not set, the script will prompt you to enter it when run.

## Running the Pipeline

```bash
python3 rag_pipeline.py
```

On **first run**, the pipeline will:
- Load the 3 PDF documents
- Split them into chunks
- Call the OpenAI Embeddings API to generate vectors
- Save the FAISS index to `faiss_index/`

On **subsequent runs**, the saved index is loaded from disk — no re-embedding needed.

To force a full rebuild of the index (e.g. after adding new PDFs):
```bash
python3 rag_pipeline.py --rebuild
```

## Sample Output

```
Loading existing FAISS index from 'faiss_index/'...

Step 4 — Building RAG chain

============================================================
Question: What is the role of a firewall in network security?
============================================================

Top 3 retrieved chunk(s):
  [1] score=0.9362 | network_security_manual.pdf — page 0
       "A firewall is the first line of defence in any network security architecture..."
  [2] score=1.1187 | network_security_manual.pdf — page 0
       "adhere to the principle of least privilege: deny all traffic by default..."
  [3] score=1.2037 | network_security_manual.pdf — page 0
       "Zone-based segmentation separates the network into logical regions..."

Answer:
A firewall serves as the first line of defence in a network security architecture...
```

> **Note on similarity scores:** FAISS returns L2 (Euclidean) distance — a **lower score means higher similarity**.

## Adding Your Own PDFs

1. Place `.pdf` files in the project directory
2. Run with `--rebuild` to re-index:
   ```bash
   python3 rag_pipeline.py --rebuild
   ```

## OpenAI Models Used

| Model | Purpose | When Called |
|---|---|---|
| `text-embedding-3-small` | Convert text to vectors | Index build + each query |
| `gpt-4o-mini` | Generate answers from retrieved context | Each query |
