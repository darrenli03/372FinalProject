# CS372 Final Project

## Miscellaneous Notes

- Could also implement a chat mode in addition to the automated excel sheet processing, that can get us this rubric item:
  - Built multi-turn conversation system with context management and history tracking (7 pts)
- fine tuning would require significant effort since we need to create the prompt/answer database ourselves

## Unmatched Rubric Items:
Core ML Fundamentals
- Modular code design with reusable functions and classes rather than monolithic scripts (3 pts)
- Created baseline model for comparison (e.g., constant prediction, random, simple heuristic) (3 pts)
    - Return random excel sheet with yes/no on everything
- Implemented data augmentation appropriate to your data modality (evidence: code + evaluation of impact) (5 pts) 
    - this could be done in the process of creating our test dataset, for example creating an example user prompt and replacing words in it with synonyms to increase our test set size

Natural Language Processing

- Applied in-context learning with few short examples or chain of thought prompting (5 pts)
- Applied prompt engineering with evaluation of multiple prompt designs (evidence: comparison table) (3 pts)
- Built retrieval-augmented generation (RAG) system with document retrieval and generation components (10 pts) 

Advanced System Integration

- Implemented production-grade deployment (evidence of at least two considerations such as rate limiting, caching, monitoring, error handling, logging) (10 pts)
- System guardrails against toxicity or inappropriate use employing at least two techniques (e.g., fine-tuning, system prompt, toxicity classifier, etc.) with evidence of impact (7 pts)
 
Model Evaluation and Analysis

- Measured and reported inference time, throughput, or computational efficiency (3 pts)
- Analyzed model behavior on edge cases or out-of-distribution examples (5 pts)
- Used at least three distinct and appropriate evaluation metrics for your task (3 pts)
- Conducted both qualitative and quantitative evaluation with thoughtful discussion (5 pts)

## TODO List:

- [X] Can mark an item done as shown here

  * [put associated rubric item(s) here]

- [ ] Extract text from pdf and chunk it 

  * Implemented comprehensive text preprocessing and tokenization pipeline (3 pts)

- [ ] Create embeddings from text chunks (decide whether to use proprietary API like OpenAI's (https://platform.openai.com/docs/models/text-embedding-3-large) or library like LangChain), retrieve relevant text sections based on embeddings when constructing query

  *  Used sentence embeddings for semantic similarity or retrieval (5 pts)

- [ ] Construct query (system prompt + context + component info), apply instruction tuning so we are able to program actions based on the response from the OpenAI API

  * Applied instruction tuning or supervised fine-tuning (SFT) for specific task format (7 pts)

- [ ] Send constructed query to OpenAI API

  * Made API calls to state-of-the-art model (GPT-4, Claude, Gemini) with meaningful integration into your system (5 pts)


- [ ] Create testing framework for evaluating model accuracy (may have to write test data classifying exports ourselves?) 

  * Collected or constructed original dataset through substantial engineering effort (e.g., API integration, web scraping, manual annotation/labeling, custom curation) with documented methodology (10 pts)

- [ ] Create frontend UI (Vite, React)
- [ ] Deploy to web via Vercel/Netlify 

  * Deployed model as functional web application with user interface (10 pts)




# Setup (using PowerShell)

## Creating Vite React frontend
```powershell
npm create vite@latest react372 -- --template react
```

## Creating Python virtual environment (run in project root)
```powershell
python -m venv venv
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
