import os
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Tuple
import chromadb
import chromadb.utils.embedding_functions as embedding_functions
import time
# import re


CHROMA_PATH = "files/chroma_db"
dbName = "ccl-embeddings"
# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# 1. Load data
def load_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# 2. Split data
def split_text(text: str, chunk_size: int = 20000, overlap: int = 2000) -> list:

    # pattern = r'Category [0-9]—(?!Part|\n)'
    #  # Split the text based on the pattern
    # sections = re.split(pattern, text)
    
    # # Create a list of documents
    # documents = [{'text': section.strip()} for section in sections if section.strip()]
    
    # return documents

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    return text_splitter.create_documents([text])

# 3. Create Chroma database
def create_chroma_db(documents: List, path: str, name: str) -> Tuple[chromadb.Collection, str]:
    chroma_client = chromadb.PersistentClient(path=path)
    
    cols = chroma_client.list_collections()
    names = [getattr(c, "name", c.get("name") if isinstance(c, dict) else repr(c)) for c in cols]
    #check if collection already exists, if so ask for confirmation before overwriting
    if name in names:
        confirm = input(f"Collection '{name}' already exists. Overwrite? (y/n): ")
        if confirm.lower() != 'y':
            print("Aborting database creation.")
            return chroma_client.get_collection(name=name), name
        else:
            chroma_client.delete_collection(name=name)
            print(f"Overwriting collection '{name}'.")

    # Create a Google Gemini embedding function for ChromaDB
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                api_key=OPENAI_API_KEY,
                model_name="text-embedding-3-small"
            )

    db = chroma_client.create_collection(name=name, embedding_function=openai_ef)
    
    for i, d in enumerate(documents):
        print(f"Adding document {i} / {len(documents)} to the database")
        try:
            db.add(documents=[d.page_content], ids=str(i))
        except Exception as e:
            print(f"Error adding document {i}: {e}")    

    return db, name

# load txt file
DOC_PATH="files/ccl.txt"
text = load_text(DOC_PATH)
# print out the first 3 lines of the text
# lines = text.splitlines()  # Split the text into lines
# for i, line in enumerate(lines[:3]):
#     print(f"{i + 1}: {line}")

chunks = split_text(text, chunk_size=1000, overlap=500)
print(chunks[0])

# Load the database for future queries
db, collection_name = create_chroma_db(documents=chunks, path=CHROMA_PATH, name=dbName)

