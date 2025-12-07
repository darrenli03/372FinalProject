from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import sys
import os
from dotenv import load_dotenv, find_dotenv
from gpt_query import generate_rag_answer

dotenv_path = find_dotenv(os.path.join("..", ".env"))
load_dotenv(dotenv_path, override = True)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.post("/query_single")
async def query_single(
    search_query: str,
):
    try:
        if not search_query:
            raise HTTPException(status_code=400, detail="Empty search query")

        result, excerpts = generate_rag_answer(search_query)
        return {"query": search_query, "response": result, "excerpts": excerpts}
    except (ValueError, BaseException) as e:
        raise e
        # raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    
    # port = int(os.environ.get("PORT", os.getenv("PORT", "8080")))
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")
