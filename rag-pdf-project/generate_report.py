from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib import colors

OUTPUT = "/Users/bsmith/Documents/AI Training/vt_agentic_ai/4 - llm_internals/project/analysis_report.pdf"

styles = getSampleStyleSheet()

title_style    = ParagraphStyle("title",    parent=styles["Title"],   fontSize=16, leading=22, spaceAfter=4)
subtitle_style = ParagraphStyle("subtitle", parent=styles["Normal"],  fontSize=11, leading=14, textColor=colors.HexColor("#555555"), spaceAfter=16, alignment=TA_CENTER)
h2_style       = ParagraphStyle("h2",       parent=styles["Heading2"],fontSize=12, leading=16, spaceBefore=14, spaceAfter=4, textColor=colors.HexColor("#1a1a2e"))
body_style     = ParagraphStyle("body",     parent=styles["Normal"],  fontSize=10, leading=14, alignment=TA_JUSTIFY, spaceAfter=6)
bullet_style   = ParagraphStyle("bullet",   parent=styles["Normal"],  fontSize=10, leading=14, leftIndent=16, spaceAfter=3)

doc = SimpleDocTemplate(
    OUTPUT, pagesize=LETTER,
    leftMargin=1*inch, rightMargin=1*inch,
    topMargin=1*inch, bottomMargin=1*inch,
)

story = []

# ── Title block ───────────────────────────────────────────────────────────────
story.append(Paragraph("RAG Pipeline: PDF Chunking and Retrieval", title_style))
story.append(Paragraph("Application Design Analysis Report", subtitle_style))
story.append(Spacer(1, 0.05*inch))

# ── 1. Overview ───────────────────────────────────────────────────────────────
story.append(Paragraph("1. Application Overview", h2_style))
story.append(Paragraph(
    "This application implements a Retrieval-Augmented Generation (RAG) pipeline that allows "
    "users to query a set of PDF documents using natural language. Rather than relying solely on "
    "a large language model's (LLM) pre-trained knowledge, the system grounds every response in "
    "content retrieved directly from the supplied documents, reducing hallucination and enabling "
    "domain-specific question answering without fine-tuning.",
    body_style))
story.append(Paragraph(
    "The pipeline is composed of five stages: (1) PDF loading via LangChain's PyPDFLoader, "
    "(2) recursive character-based text chunking, (3) vector embedding using OpenAI's "
    "text-embedding-3-small model, (4) local FAISS vector storage and similarity search, and "
    "(5) answer generation via gpt-4o-mini conditioned on the retrieved context.",
    body_style))

# ── 2. Architecture Summary ───────────────────────────────────────────────────
story.append(Paragraph("2. Architecture Summary", h2_style))

table_data = [
    ["Component", "Technology", "Role"],
    ["Document Loader",   "LangChain PyPDFLoader",          "Parses PDF files into page-level Document objects"],
    ["Text Splitter",     "RecursiveCharacterTextSplitter",  "Splits pages into 500-char chunks with 50-char overlap"],
    ["Embedding Model",   "OpenAI text-embedding-3-small",   "Converts text to 1,536-dim float vectors"],
    ["Vector Store",      "FAISS (local, CPU)",              "Indexes vectors and performs cosine similarity search"],
    ["LLM",               "OpenAI gpt-4o-mini",              "Generates answers from retrieved context"],
    ["Orchestration",     "LangChain Core",                  "Chains retriever, prompt, LLM, and output parser"],
]

table = Table(table_data, colWidths=[1.3*inch, 2.1*inch, 3.0*inch])
table.setStyle(TableStyle([
    ("BACKGROUND",  (0,0), (-1,0),  colors.HexColor("#1a1a2e")),
    ("TEXTCOLOR",   (0,0), (-1,0),  colors.white),
    ("FONTNAME",    (0,0), (-1,0),  "Helvetica-Bold"),
    ("FONTSIZE",    (0,0), (-1,-1), 8.5),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.HexColor("#f5f5f5"), colors.white]),
    ("GRID",        (0,0), (-1,-1), 0.4, colors.HexColor("#cccccc")),
    ("VALIGN",      (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING",  (0,0), (-1,-1), 5),
    ("BOTTOMPADDING",(0,0),(-1,-1), 5),
    ("LEFTPADDING", (0,0), (-1,-1), 6),
]))
story.append(table)

# ── 3. OpenAI API Calls ───────────────────────────────────────────────────────
story.append(Paragraph("3. OpenAI API Calls", h2_style))
story.append(Paragraph(
    "The pipeline makes three distinct calls to the OpenAI API. The first call (index build) "
    "embeds all document chunks in batch and occurs only once — results are persisted to disk. "
    "The second and third calls occur on every user query: the question is embedded for "
    "similarity search, and the retrieved context plus question are sent to the chat completions "
    "endpoint for answer generation. The FAISS similarity search itself runs entirely locally "
    "with no API involvement.",
    body_style))

# ── 4. Pros ───────────────────────────────────────────────────────────────────
story.append(Paragraph("4. Design Strengths", h2_style))
pros = [
    ("<b>Grounded responses:</b> Answers are derived from retrieved document content, "
     "significantly reducing LLM hallucination compared to prompt-only approaches."),
    ("<b>Persistent index:</b> The FAISS index is saved to disk after the first build. "
     "Subsequent runs load it instantly, eliminating redundant embedding API calls and cost."),
    ("<b>Local vector storage:</b> FAISS runs on-device with no external database dependency, "
     "keeping retrieval fast, private, and free beyond the initial embedding cost."),
    ("<b>Source transparency:</b> Retrieved chunks are displayed with their source filename "
     "and page number alongside a similarity score, making answers auditable and traceable."),
    ("<b>Portability:</b> The pipeline runs identically on a local machine and Google Colab "
     "with no infrastructure changes — a single install script handles dependencies."),
    ("<b>Modular design:</b> Each stage (load, chunk, embed, index, query) is an independent "
     "function, making it straightforward to swap components — e.g., a different embedding "
     "model or a different vector store."),
]
for p in pros:
    story.append(Paragraph(f"• {p}", bullet_style))

# ── 5. Cons ───────────────────────────────────────────────────────────────────
story.append(Paragraph("5. Design Limitations", h2_style))
cons = [
    ("<b>Fixed chunk size:</b> The 500-character chunk size is a static heuristic. Chunks "
     "that split mid-sentence or mid-table can degrade retrieval quality. Semantic or "
     "sentence-aware chunking would improve coherence."),
    ("<b>No re-ranking:</b> Retrieval relies solely on vector similarity (L2 distance). "
     "A cross-encoder re-ranker applied after initial retrieval would improve precision, "
     "especially for ambiguous queries."),
    ("<b>Top-k only:</b> The pipeline always retrieves exactly k=3 chunks regardless of "
     "their relevance scores. A score threshold would prevent low-quality chunks from "
     "being included in the context."),
    ("<b>Single-turn queries:</b> There is no conversation memory. Each question is answered "
     "independently, so follow-up questions that reference prior answers are not supported."),
    ("<b>PDF text extraction limits:</b> PyPDFLoader extracts plain text only. Scanned PDFs, "
     "tables, figures, and complex layouts may be extracted poorly or lost entirely."),
    ("<b>OpenAI dependency:</b> Both embedding and generation require an active OpenAI API "
     "key with sufficient credits. The pipeline cannot run fully offline."),
]
for c in cons:
    story.append(Paragraph(f"• {c}", bullet_style))

# ── 6. Conclusion ─────────────────────────────────────────────────────────────
story.append(Paragraph("6. Conclusion", h2_style))
story.append(Paragraph(
    "This RAG pipeline demonstrates a practical and cost-effective approach to document-grounded "
    "question answering. The combination of local FAISS storage, persistent indexing, and "
    "OpenAI's embedding and chat models provides a strong baseline suitable for academic and "
    "small-scale production use. Key areas for improvement include semantic chunking, "
    "retrieval re-ranking, score thresholding, and multi-turn conversation support — each of "
    "which would meaningfully increase answer quality and user experience at modest additional complexity.",
    body_style))

doc.build(story)
print(f"Report saved to {OUTPUT}")
