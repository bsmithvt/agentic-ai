"""
RAG Pipeline — PDF Chunking, FAISS Indexing, and Retrieval
-----------------------------------------------------------
Requires:  OPENAI_API_KEY environment variable
           pip install -r requirements.txt
"""

import argparse
import os
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# ── Configuration ─────────────────────────────────────────────────────────────

PDF_DIR   = Path(__file__).parent
INDEX_DIR = PDF_DIR / "faiss_index"

EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL      = "gpt-4o-mini"

CHUNK_SIZE    = 500
CHUNK_OVERLAP = 50

# ── Step 1: Load PDFs ─────────────────────────────────────────────────────────

def load_documents(pdf_dir: Path) -> list:
    pdf_files = sorted(pdf_dir.glob("*.pdf"))
    if not pdf_files:
        raise FileNotFoundError(f"No PDF files found in {pdf_dir}")

    docs = []
    for pdf_path in pdf_files:
        loader = PyPDFLoader(str(pdf_path))
        pages  = loader.load()
        docs.extend(pages)
        print(f"  Loaded '{pdf_path.name}' ({len(pages)} page(s))")

    print(f"Total pages loaded: {len(docs)}")
    return docs

# ── Step 2: Chunk documents ───────────────────────────────────────────────────

def chunk_documents(docs: list) -> list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(docs)
    print(f"Total chunks created: {len(chunks)}")
    return chunks

# ── Step 3: Build or load FAISS index ─────────────────────────────────────────

def build_index(chunks: list, embeddings: OpenAIEmbeddings) -> FAISS:
    print("Generating embeddings and building FAISS index...")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(str(INDEX_DIR))
    print(f"Index saved to '{INDEX_DIR}'")
    return vectorstore


def load_index(embeddings: OpenAIEmbeddings) -> FAISS:
    print(f"Loading existing FAISS index from '{INDEX_DIR}'...")
    return FAISS.load_local(str(INDEX_DIR), embeddings, allow_dangerous_deserialization=True)


def get_vectorstore(embeddings: OpenAIEmbeddings, rebuild: bool = False) -> FAISS:
    if not rebuild and INDEX_DIR.exists():
        return load_index(embeddings)

    print("No existing index found (or --rebuild requested) — building from scratch")
    print("\nStep 1 — Loading PDFs")
    docs   = load_documents(PDF_DIR)
    print("\nStep 2 — Chunking documents")
    chunks = chunk_documents(docs)
    print("\nStep 3 — Building FAISS index")
    return build_index(chunks, embeddings)

# ── Step 4: Build RAG chain ───────────────────────────────────────────────────

PROMPT_TEMPLATE = """You are a helpful assistant. Answer the question using ONLY the context below.
If the answer is not in the context, say "I don't have enough information to answer that."

Context:
{context}

Question: {question}
"""

def build_rag_chain(vectorstore: FAISS, llm: ChatOpenAI):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    def format_docs(docs):
        return "\n\n---\n\n".join(
            f"[Source: {d.metadata.get('source', 'unknown')}, page {d.metadata.get('page', '?')}]\n{d.page_content}"
            for d in docs
        )

    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain, retriever

# ── Step 5: Query helper ───────────────────────────────────────────────────────

def query(chain, vectorstore: FAISS, question: str) -> None:
    print(f"\n{'='*60}")
    print(f"Question: {question}")
    print(f"{'='*60}")

    results = vectorstore.similarity_search_with_score(question, k=3)
    print(f"\nTop {len(results)} retrieved chunk(s):")
    for i, (doc, score) in enumerate(results, 1):
        src  = Path(doc.metadata.get("source", "?")).name
        page = doc.metadata.get("page", "?")
        print(f"  [{i}] score={score:.4f} | {src} — page {page}")
        print(f"       \"{doc.page_content[:120].strip()}...\"")

    answer = chain.invoke(question)
    print(f"\nAnswer:\n{answer}")

# ── Main ───────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="RAG pipeline over local PDF documents.")
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Force re-embedding and rebuild the FAISS index even if one already exists on disk.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        api_key = input("Enter your OpenAI API key: ").strip()
        os.environ["OPENAI_API_KEY"] = api_key

    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    llm        = ChatOpenAI(model=CHAT_MODEL, temperature=0)

    vectorstore = get_vectorstore(embeddings, rebuild=args.rebuild)

    print("\nBuilding RAG chain")
    chain, _ = build_rag_chain(vectorstore, llm)

    questions = [
        "What is the role of a firewall in network security?",
        "How much has global sea level risen since 1993?",
        "What is the difference between an IDS and an IPS?",
        "How does the transformer architecture handle long-range dependencies?",
        "What chunking strategies are recommended for RAG pipelines?",
    ]

    for q in questions:
        query(chain, vectorstore, q)


if __name__ == "__main__":
    main()
