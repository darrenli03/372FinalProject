# CS372 Final Project

## What it Does

This project is a retrieval-augmented generation (RAG) pipeline that creates embeddings from the Commerce Control List (pdf available for download at https://www.ecfr.gov/current/title-15/subtitle-B/chapter-VII/subchapter-C/part-774/appendix-Supplement%20No.%201%20to%20Part%20774), then uses those embeddings to decide whether user-provided products/components (for example: ceramic body armor plates) are restricted or not. Future plans include multi-component processing via excel and including the ITAR in the embeddings.

## Quick Start (Developers)

- **Backend (PowerShell):** create and activate a Python virtualenv, install backend requirements, then run the server:

```
python -m venv .venv_new; .\.venv_new\Scripts\Activate.ps1
pip install -r backend\requirements.txt
python backend\server.py
```

- **Frontend (PowerShell):** install node modules and start the dev server from the `frontend` folder:
  - Note: you will have to change the fetch endpoint in [App.jsx](https://github.com/darrenli03/372FinalProject/blob/main/frontend/src/App.jsx) to the localhost endpoint: "http://127.0.0.1:8080/query_single?search_query=${encoded}" 

```
cd frontend; npm install; npm run dev
```

## Video Links

- Non-technical demo video: [linked here](https://youtu.be/20f0HVoEuMw)
- Technical walkthrough: [linked here](https://youtu.be/eLkqJT3o3_U)

## Evaluation


## Individual Contributions

- Darren Li
  - Backend: RAG pipeline `doc_embedding.py`, including Pinecone vector store integration (`pinecone_upload.py`), OpenAI integration (`gpt_query.py`) and server API endpoints (`server.py`)
  - Frontend: React app and UI (`frontend/src` components) implementation and integration with backend API
  - Additional work: Setting up AWS EC2 instance (Nginx and HTTPS certificate configuration), deploying frontend on Vercel (DNS configuration) with DoS protection via Cloudflare
- Andy Li
  - PDF processing (`text_extractor.py`)
  - testing dataset curation [linked here](https://docs.google.com/spreadsheets/d/1KOmhZdAN5oiNj53-cfMunaYKK5Qf9fVJdLKmyaLzLyc/edit?usp=sharing)
  - manual testing of model performance for items in testing dataset 
  - analyzing results quantitatively and qualitatively

## Miscellaneous Notes

- Could also implement a chat mode in addition to the automated excel sheet processing, that can get us this rubric item:
  - Built multi-turn conversation system with context management and history tracking (7 pts)
- fine tuning would require significant effort since we need to create the prompt/answer database ourselves
- To regenerate the database, boot up the virtual environment with the requirements from backend/requirements.txt, first run doc_embedding.py (text_extractor.py generated files/ccl.txt that is already version controlled, but may need to be updated as the legal body updates) (this will likely take an hour or two), then run pinecone_upload.py to replace the old index in pinecone with the new embeddings (perhaps about 10 minutes?)
