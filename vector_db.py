import numpy as np
from supabase_client import supabase

def fake_embed(text: str):
    """
    Replace with real embedding model later
    """
    return np.random.rand(1536).tolist()

def fetch_from_embeddings(query: str):
    query_embedding = fake_embed(query)

    response = supabase.rpc(
        "match_embeddings",
        {
            "query_embedding": query_embedding,
            "match_threshold": 0.75,
            "match_count": 3
        }
    ).execute()

    if not response.data:
        return None

    return response.data[0]["content"]
