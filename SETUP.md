# Setup

**Backend (PowerShell):** 
1. In project root, create and activate a Python virtual environment (named .venv), install backend requirements, then run the server:

```
python -m venv .venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
.\.venv_new\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r backend\requirements.txt
python backend\server.py
```
Alternatively, in VSCode, Press Ctrl+Shift+P → "Python: Select Interpreter", click through to set up virtual environment

2. You will also have to create a .env file in backend with these categories (get the OpenAI key from the OpenAI [developer dashboard](https://platform.openai.com/docs/overview), Pinecone API from [pinecone.io](https://www.pinecone.io/), and a string that represents whatever you named the Pinecone Index). It will look like this:
```
OPENAI_API_KEY=[insert OpenAI API key here, no quotes around it]
PINECONE_API_KEY=[insert Pinecone API key here, no quotes around it]
PINECONE_INDEX="[insert index name, for example OpenAI-rag-embeddings]" 
```
  

**Frontend (PowerShell):** 
- Install node modules and start the dev server from the `frontend` folder:

```
cd frontend
npm install 
npm run dev
```
- To test locally, change the fetch endpoint in [App.jsx](https://github.com/darrenli03/372FinalProject/blob/main/frontend/src/App.jsx) to the localhost endpoint: "http://127.0.0.1:8080/query_single?search_query=${encoded}"

## Miscellaneous Notes 
### Activating Virtual Environment (Powershell)
```powershell
.\venv\Scripts\Activate.ps1
```

### Export current requirements to requirements.txt
```powershell
pip freeze > requirements.txt
```

