#chromadb debugging
# from chromadb.utils import embedding_functions
# import chromadb

# def list_chroma_collections(path: str = "files/chroma_db") -> list:
#     """
#     Return a list of collection names in the Chroma persistent client at `path`.
#     """
#     client = chromadb.PersistentClient(path=path)
#     cols = client.list_collections()
    
#     if not cols:
#         print('No collections found.')
#     else:
#         print(f"Found {len(cols)} collections:")
    
#     # names = []
#     # for c in cols:
#     #     # chromadb versions may return objects or dicts
#     #     if hasattr(c, "name"):
#     #         names.append(c.name)
#     #     elif isinstance(c, dict) and "name" in c:
#     #         names.append(c["name"])
#     #     else:
#     #         names.append(repr(c))
#     # return names

#     return [getattr(c, "name", c.get("name") if isinstance(c, dict) else repr(c)) for c in cols]
# print(list_chroma_collections())





#testing openai embbedding, pinecone query, and gpt query
# from openai import OpenAI
# import os
# from dotenv import load_dotenv, find_dotenv
# from pinecone import Pinecone

# load_dotenv(find_dotenv())

# # OpenAI client (embeddings + chat)
# client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# # Pinecone configuration
# PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
# PINECONE_INDEX = os.environ.get("PINECONE_INDEX", "ccl-embeddings-openaismall")

# pine_client = Pinecone(api_key=PINECONE_API_KEY) if PINECONE_API_KEY else None
# pine_index = pine_client.Index(PINECONE_INDEX) if pine_client is not None else None


# def embed_text(text: str, model: str = "text-embedding-3-small"):
#     """Return OpenAI embedding for text."""
#     resp = client.embeddings.create(model=model, input=text)
#     return resp.data[0].embedding


# def get_relevant_passage(query: str, n_results: int = 4):
#     """Embed the query with OpenAI, query Pinecone, and return the top matched passages as a list."""
#     if pine_index is None:
#         raise RuntimeError("Pinecone index not configured. Set PINECONE_API_KEY and PINECONE_INDEX.")

#     embedding = embed_text(query)
#     print("--------------------------------------embedding completed--------------------------------------")
#     # print(embedding)
#     # Query Pinecone using the embedding
#     try:
#         pinecone_response = pine_index.query(vector = embedding, top_k=n_results, include_metadata=True, include_values=False)
#     except TypeError:
#         pinecone_response = pine_index.query(vector = embedding, top_k=n_results, include_metadata=True)

#     if not pinecone_response:
#         print("--------------------------------------no response from pinecone--------------------------------------")
#         return []
#     # From pinecone_response, extract `chunk_text` from metadata of each match
#     passages = []

#     # The Pinecone response may be a dict or an object with a `.matches` attribute.
#     if hasattr(pinecone_response, "matches"):
#         #this is what is expected
#         matches = pinecone_response.matches
#         # print("matches found")
#     else:
#         print("Pinecone API response does not include matches attribute, aborting")
#         return []
#     for m in matches:
#         # metadata may be an attribute or a dict
#         metadata = getattr(m, "metadata", None)
#         if metadata is None and isinstance(m, dict):
#             metadata = m.get("metadata", {})

#         if not metadata:
#             continue

#         # metadata is expected to be a dict with field "text" that we want to extract
#         chunk_text = None
#         if isinstance(metadata, dict):
#             print("------------------metadata is a dict------------------")
#             # print(metadata)
#             chunk_text = metadata["text"]
#             # chunk_text = metadata.get("chunk_text")
#         else:
#             print("metadata not a dict as expected")
#             continue

#         if chunk_text:
#             passages.append(chunk_text)

#     return passages

# passages = get_relevant_passage("night vision goggles", n_results=4)

# for i in passages:
#     print(i)
#     print("\n---\n")



#test client for server API
import sys
import json
import urllib.request
import urllib.parse
from urllib.error import URLError, HTTPError

def main():
    query = "night vision goggles" if len(sys.argv) == 1 else " ".join(sys.argv[1:])
    encoded = urllib.parse.quote_plus(query)
    url = f"http://localhost:8000/query_single?search_query={encoded}"
    req = urllib.request.Request(url, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode("utf-8")
            try:
                obj = json.loads(body)
                print(json.dumps(obj, indent=2, ensure_ascii=False))
            except json.JSONDecodeError:
                print("Non-JSON response:")
                print(body)
    except HTTPError as e:
        print(f"HTTP error: {e.code} {e.reason}")
        print(e.read().decode(errors="ignore"))
    except URLError as e:
        print(f"Connection error: {e.reason}")

if __name__ == "__main__":
    main()