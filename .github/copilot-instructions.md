<!-- .github/copilot-instructions.md -->
# Copilot / AI agent instructions — 372FinalProject

Purpose: give an AI coding agent the minimal, actionable context needed to work in this repo.

- Project shape (big picture)
  - This repo is a small prototype RAG pipeline kept under `backend/`.
  - Important files:
    - `backend/text_extractor.py` — notebook-style code to extract text from a PDF and chunk it (`chunk_text`).
    - `backend/gpt_query.py` — notebook-style RAG pipeline: embed chunks with SentenceTransformers, build a FAISS index, retrieve similar chunks, and run `classify_from_context` + `legal_rag` which returns a dict `{query, classification, top_chunks, similarity_scores}`.
    - `backend/rag_document_picker` — currently an empty placeholder (intended to pick which docs to include in RAG).
    - `backend/server.py` — empty placeholder (likely where an API/server should be implemented).

- Data flow / responsibilities
  - PDF file -> `text_extractor.py` (reads `PDF_PATH`, extracts text, calls `chunk_text`).
  - Chunks -> SentenceTransformer model (`all-MiniLM-L6-v2`) -> normalized float32 embeddings.
  - Embeddings -> FAISS `IndexFlatIP` (inner product similarity) stored in-memory.
  - Query -> `retrieve_similar()` -> top chunks + scores -> `classify_from_context()` -> `legal_rag()` response.

- Project-specific conventions & gotchas
  - The two backend scripts are written in notebook style and include "!pip install ..." lines. These will fail in a plain `python file.py` run. Either:
    - Run them inside a Jupyter/Colab session, or
    - Remove the leading `!` and install packages in a venv first (see "Run / debug" below).
  - Default PDF path in both scripts: `/mnt/data/indexccl.pdf`. Update `PDF_PATH` when testing locally.
  - Embeddings are normalized and stored as float32; FAISS uses `IndexFlatIP` which expects normalized vectors for cosine-like ranking.

- Key functions to reference in edits/tests
  - `text_extractor.chunk_text(text, max_chars=1000)` — chunking logic (default ~1000 chars).
  - `gpt_query.retrieve_similar(query, k=5)` — returns `(chunks, scores)`.
  - `gpt_query.classify_from_context(query, retrieved)` — simple rule-based classifier (looks for words like "prohibited", "illegal", "controlled", "license", "eccn").
  - `gpt_query.legal_rag(query, k=5)` — top-level pipeline; returns a dict ready for API responses.

- How to run / debug (concrete)
  - Quick interactive test (recommended): open a Python REPL or Jupyter notebook, copy the contents of `gpt_query.py`/`text_extractor.py`, install packages, set `PDF_PATH` to a local file, then call:
    - `chunks = chunk_text(<text>)`
    - `result = legal_rag("your question here")`
  - To run as a script locally:
    - Create a venv, then: `pip install pdfplumber sentence-transformers faiss-cpu`
    - Remove or edit the `!pip install ...` lines from the files.
    - Set `PDF_PATH` to a valid path and add a `if __name__ == "__main__":` wrapper if you want script behavior.

- Integration points / TODOs for future work (explicit, discoverable)
  - `server.py` should implement an HTTP API that calls `legal_rag()` — currently empty.
  - `rag_document_picker` should encapsulate logic for selecting which PDFs/docs to index or query.
  - Persisting a FAISS index and reloading it (instead of rebuilding on every run) will be necessary for production.

- Debug tips for AI agents
  - Look for `!pip install`—if present, assume notebook origin and either run interactively or sanitize for scripts.
  - Search for `PDF_PATH` to find where test data is wired in; update paths before running.
  - When changing embedding/model code, maintain the normalized float32 contract; FAISS index configuration (dim, IndexFlatIP) must align with embedding dims.

If any of the placeholders (`server.py`, `rag_document_picker`) should follow a specific framework (FastAPI/Flask) or if you want a `requirements.txt` added, tell me which one to target and I will scaffold it and wire a minimal API that calls `legal_rag()`.

Please review and tell me if any section is unclear or missing — I can iterate quickly with more file-level details or add runnable scaffolding.
