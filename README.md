# CS372 Final Project

## Miscellaneous Notes

- Could also implement a chat mode in addition to the automated excel sheet processing, that can get us this rubric item:
  - Built multi-turn conversation system with context management and history tracking (7 pts)
- fine tuning would require significant effort since we need to create the prompt/answer database ourselves
- To regenerate the database, boot up the virtual environment with the requirements from backend/requirements.txt, first run doc_embedding.py (text_extractor.py generated files/ccl.txt that is already version controlled, but may need to be updated as the legal body updates) (this will likely take an hour or two), then run pinecone_upload.py to replace the old index in pinecone with the new embeddings (perhaps about 10 minutes?)

## Unmatched Rubric Items:
Core ML Fundamentals

- Implemented data augmentation appropriate to your data modality (evidence: code + evaluation of impact) (5 pts) 
    - this could be done in the process of creating our test dataset, for example creating an example user prompt and replacing words in it with synonyms to increase our test set size

Natural Language Processing

Advanced System Integration

- System guardrails against toxicity or inappropriate use employing at least two techniques (e.g., fine-tuning, system prompt, toxicity classifier, etc.) with evidence of impact (7 pts)
 
Model Evaluation and Analysis



## TODO List: (total points so far: -7 if we don't include excel sheet processing)

points: 
3 for modular code
3 + 5 for extracting and chunking text
5 + 5 + 3 for generating and using embeddings and prompt engineering (chain of thought AND in context learning)
5 + 10 for sending the query to OpenAI (RAG)
7 for excel processing (Maybe)
10 for production grade deployment
10 for deploying to web (WIP)
3 for baseline model (WIP)
10 for curating test database 
79 total (72 without excel) (62 without excel and assuming 0 on production grade deployment)

model evaluation: 
3 + 5 + 3 + 5 = 16

- [X] Can mark an item done as shown here

  * [put associated rubric item(s) here]

- [X] organize code into functions

  * Modular code design with reusable functions and classes rather than monolithic scripts (3 pts)

- [X] Extract text from pdf and chunk it 

  * Implemented comprehensive text preprocessing and tokenization pipeline (3 pts)
    * extracts text from pdf using pdfplumber
  * Used a significant software framework for applied ML not covered in the class (e.g., instead of PyTorch, used Tensorflow; or used JAX, LangChain, etc. not covered in detail in the class) (5 pts)
    * chunking uses Langchain RecursiveCharacterTextSplitter

- [X] Create embeddings from text chunks (decide whether to use proprietary API like OpenAI's (https://platform.openai.com/docs/models/text-embedding-3-large) or library like LangChain), retrieve relevant text sections based on embeddings when constructing query

  *  Used sentence embeddings for semantic similarity or retrieval (5 pts)

- [X] Create query (system prompt + context + component info), apply in-context learning (one shot probably) so we are able to program actions based on the response from the OpenAI API

  * Applied in-context learning with few short examples or chain of thought prompting (5 pts)
  * Applied prompt engineering with evaluation of multiple prompt designs (evidence: comparison table) (3 pts)

- [X] Send constructed query to OpenAI API

  * Made API calls to state-of-the-art model (GPT-4, Claude, Gemini) with meaningful integration into your system (5 pts)
  * Built retrieval-augmented generation (RAG) system with document retrieval and generation components (10 pts) 

- [ ] Process an entire excel sheet of queries

  * Implemented agentic system where model outputs trigger automated actions or tool calls (e.g., function calling, database writes, API integrations) (7 pts)

- [ ] create server code that exposes API endpoints for frontend to call, as well as does rate limiting

  * Implemented production-grade deployment (evidence of at least two considerations such as rate limiting, caching, monitoring, error handling, logging) (10 pts)
    * pinecone does auto scaling based on load, vercel/netlify also offer this feature for frontend, could also add CI/CD pipeline, logging, user logins for rate limiting, and more
  
- [ ] Create testing framework for evaluating model accuracy (may have to write test data classifying exports ourselves?) 

  * Collected or constructed original dataset through substantial engineering effort (e.g., API integration, web scraping, manual annotation/labeling, custom curation) with documented methodology (10 pts)
  * Created baseline model for comparison (e.g., constant prediction, random, simple heuristic) (3 pts)
    * Return random excel sheet with yes/no on everything

- [ ] Create frontend UI (Vite, React)

  * Must allow user to upload excel sheet which will be sent to backend for processing
  * Must allow user to also submit small text queries of a item to be processed
  * Should have some waiting page while the excel sheet is processing
  * return either a modified excel sheet (column added for appropriate tags of each product in sheet) or a text list of all items that are restricted
  * Should have safeguards (debouncing button presses, rate limiting on server side)

- [ ] Deploy to web via Vercel/Netlify 

  * Deployed model as functional web application with user interface (10 pts)

- [ ] Evaluate performance (based on these rubric items)

  * Measured and reported inference time, throughput, or computational efficiency (3 pts) 
  * Analyzed model behavior on edge cases or out-of-distribution examples (5 pts)
  * Used at least three distinct and appropriate evaluation metrics for your task (3 pts)
  * Conducted both qualitative and quantitative evaluation with thoughtful discussion (5 pts)

# Setup (using PowerShell)

## Creating Vite React frontend
```powershell
npm create vite@latest react372 -- --template react
```

## Creating Python virtual environment (run in project root)
```powershell
python -m venv venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
```
Alternatively, 
- Press Ctrl+Shift+P → "Python: Select Interpreter", click through to set up virtual environment

## Activate virtual environment
```powershell
.\venv\Scripts\Activate.ps1
```

## Export current requirements to requirements.txt
```powershell
pip freeze > requirements.txt
```

## Install from requirements.txt
```powershell
pip install -r requirements.txt
```
