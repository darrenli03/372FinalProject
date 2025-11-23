from openai import OpenAI
import os
from dotenv import load_dotenv, find_dotenv
import chromadb
import chromadb.utils.embedding_functions as embedding_functions

CHROMA_PATH = "files/chroma_db"
dbName = "ccl-embeddings"

load_dotenv(find_dotenv())
client = OpenAI(api_key=os.environ.get("PINECONE_API_KEY"))

# Function to load Chroma collection
def load_chroma_collection(path: str, name: str):
    """
    Loads an existing Chroma collection from the specified path with the given name.
    """
    chroma_client = chromadb.PersistentClient(path=path)
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                api_key=os.environ.get("OPENAI_API_KEY"),
                model_name="text-embedding-3-small"
                )
    return chroma_client.get_collection(name=name, embedding_function=openai_ef)


# Retrieval from ChromaDB
def get_relevant_passage(query, db, n_results):
    """
    Retrieve relevant passages for the given query from the database.
    """
    passages = db.query(query_texts=[query], n_results=n_results)['documents'][0]
    # print(passages, "\n")
    return passages

# Make prompt for generative model
def make_rag_prompt(query, relevant_passage):
    """
    Constructs an optimized chain-of-thought RAG prompt
    for export-control classification using CCL passages.
    """
    escaped = relevant_passage.replace("'", "").replace('"', "").replace("\n", " ")

    prompt = f"""
You are an expert export-control compliance analyst specializing in the U.S. Commerce Control List (CCL).
Your task is to classify products, components, or technical descriptions strictly using the provided CONTEXT.

Follow this reasoning process implicitly (do NOT reveal it in your final answer):
1. Break down the query into key technical characteristics.
2. Compare those characteristics to the control criteria in the CONTEXT.
3. Identify any matching thresholds, performance parameters, material specifications, or definitions.
4. Decide if the item is described, controlled, partially controlled, or not controlled according to the CONTEXT.
5. Formulate a concise, direct answer *without revealing your reasoning steps*.

Rules:
- Use ONLY the information found in the CONTEXT.
- If the CONTEXT does not provide enough information to classify the item, respond with: "I don't know."
- Do NOT hallucinate missing thresholds, materials, or ECCNs.
- Do NOT justify your reasoning or explain the steps.
- Do NOT mention chain of thought.
- At the end, include a short citation of the exact lines/phrases from the CONTEXT that support your conclusion.

---
CONTEXT:
{escaped}

QUERY:
{query}

---
Provide:
1. **A clear classification answer** (e.g., “This item matches the description of …” or “The context does not include information to classify this item.”)
2. **A 1–2 sentence explanation referencing only the provided context**
3. **A quotation of the specific context lines that support your answer**
"""
    return prompt


# Final function to integrate all steps
def generate_rag_answer(query):
    db = load_chroma_collection(path=CHROMA_PATH, name=dbName)

    # Retrieve most relevant text chunk
    relevant_texts = get_relevant_passage(query, db, n_results=4)
    # print("relevant texts: \n", relevant_texts)
    prompt = make_rag_prompt(query, relevant_passage="".join(relevant_texts))  # Joining the relevant chunks
        
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": prompt}
    ],
    temperature=0.7
    )

    return response.choices[0].message.content

# Example usage
if __name__ == "__main__":
    user_query = "plutonium fuel rods"
    answer = generate_rag_answer(user_query)
    print("Answer:\n", answer)
