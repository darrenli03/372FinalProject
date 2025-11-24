from pinecone import Pinecone, ServerlessSpec
import os
from dotenv import load_dotenv
from chromadb import PersistentClient

load_dotenv()
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
pc = Pinecone(api_key=PINECONE_API_KEY)

def migrate_chroma_to_pinecone(chroma_path, collection_name, pinecone_index_name):
    chroma_client = PersistentClient(path=chroma_path)
    collection = chroma_client.get_collection(name=collection_name)
    
    all_data = collection.get(include=['embeddings', 'documents', 'metadatas'])
    
    if pinecone_index_name not in pc.list_indexes().names():
        pc.create_index(
            name=pinecone_index_name,
            dimension=len(all_data['embeddings'][0]),
            metric='cosine',
            spec=ServerlessSpec(cloud="aws",region="us-east-1")
        )
    
    index = pc.Index(pinecone_index_name)
    
    vectors = [
        (str(i), embedding, {'text': doc})
        for i, (embedding, doc) in enumerate(zip(
            all_data['embeddings'], 
            all_data['documents']
        ))
    ]
    
    batch_size = 100
    for i in range(0, len(vectors), batch_size):
        batch = vectors[i:i + batch_size]
        index.upsert(vectors=batch)
    
    return len(vectors)

migrate_chroma_to_pinecone("files/chroma_db","ccl-embeddings","ccl-embeddings-openaismall")