from chromadb.utils import embedding_functions
import chromadb

def list_chroma_collections(path: str = "files/chroma_db") -> list:
    """
    Return a list of collection names in the Chroma persistent client at `path`.
    """
    client = chromadb.PersistentClient(path=path)
    cols = client.list_collections()
    
    if not cols:
        print('No collections found.')
    else:
        print(f"Found {len(cols)} collections:")
    
    # names = []
    # for c in cols:
    #     # chromadb versions may return objects or dicts
    #     if hasattr(c, "name"):
    #         names.append(c.name)
    #     elif isinstance(c, dict) and "name" in c:
    #         names.append(c["name"])
    #     else:
    #         names.append(repr(c))
    # return names

    return [getattr(c, "name", c.get("name") if isinstance(c, dict) else repr(c)) for c in cols]
print(list_chroma_collections())