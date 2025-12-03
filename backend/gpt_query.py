from openai import OpenAI
import os
from dotenv import load_dotenv, find_dotenv
from pinecone import Pinecone

load_dotenv(find_dotenv())

# OpenAI client (embeddings + chat)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Pinecone configuration
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_INDEX = os.environ.get("PINECONE_INDEX", "ccl-embeddings-openaismall")

pine_client = Pinecone(api_key=PINECONE_API_KEY) if PINECONE_API_KEY else None
pine_index = pine_client.Index(PINECONE_INDEX) if pine_client is not None else None


# # Function to load Chroma collection
# def load_chroma_collection(path: str, name: str):
#     """
#     Loads an existing Chroma collection from the specified path with the given name.
#     """
#     chroma_client = chromadb.PersistentClient(path=path)
#     openai_ef = embedding_functions.OpenAIEmbeddingFunction(
#                 api_key=os.environ.get("OPENAI_API_KEY"),
#                 model_name="text-embedding-3-small"
#                 )
#     return chroma_client.get_collection(name=name, embedding_function=openai_ef)


def embed_text(text: str, model: str = "text-embedding-3-small"):
    """Return OpenAI embedding for text."""
    resp = client.embeddings.create(model=model, input=text)
    return resp.data[0].embedding


def get_relevant_passage(query: str, n_results: int = 4):
    """Embed the query with OpenAI, query Pinecone, and return the top matched passages as a list."""
    if pine_index is None:
        raise RuntimeError("Pinecone index not configured. Set PINECONE_API_KEY and PINECONE_INDEX.")

    embedding = embed_text(query)
    print("--------------------------------------embedding completed--------------------------------------")
    # print(embedding)
    # Query Pinecone using the embedding
    try:
        pinecone_response = pine_index.query(vector = embedding, top_k=n_results, include_metadata=True, include_values=False)
    except TypeError:
        pinecone_response = pine_index.query(vector = embedding, top_k=n_results, include_metadata=True)

    if not pinecone_response:
        print("--------------------------------------no response from pinecone--------------------------------------")
        return []
    # From pinecone_response, extract `chunk_text` from metadata of each match
    passages = []

    # The Pinecone response may be a dict or an object with a `.matches` attribute.
    if hasattr(pinecone_response, "matches"):
        #this is what is expected
        matches = pinecone_response.matches
        # print("matches found")
    else:
        print("Pinecone API response does not include matches attribute, aborting")
        return []
    for m in matches:
        # metadata may be an attribute or a dict
        metadata = getattr(m, "metadata", None)
        if metadata is None and isinstance(m, dict):
            metadata = m.get("metadata", {})

        if not metadata:
            continue

        # metadata is expected to be a dict with field "text" that we want to extract
        chunk_text = None
        if isinstance(metadata, dict):
            # print("------------------metadata is a dict------------------")
            # print(metadata)
            chunk_text = metadata["text"]
            # chunk_text = metadata.get("chunk_text")
        else:
            print("metadata not a dict as expected")
            continue

        if chunk_text:
            passages.append(chunk_text)

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
1. **A clear classification answer** (e.g., "Final Answer: Yes" or "Final Answer: No" or "Final Answer: I don't know")
2. **A 1–2 sentence explanation referencing only the provided context**
3. **A quotation of the specific context lines that support your answer**
"""
    return prompt


# Final function to integrate all steps
def generate_rag_answer(query):
    # Retrieve most relevant text chunks from Pinecone
    relevant_texts = get_relevant_passage(query, n_results=4)
    prompt = make_rag_prompt(query, relevant_passage="\n\n".join(relevant_texts))  # Joining the relevant chunks
    
    print(prompt)
    
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
    user_query = "Military-grade night-vision goggles (Gen-3 NVGs)"
    answer = generate_rag_answer(user_query)
    print("Answer:\n", answer)
