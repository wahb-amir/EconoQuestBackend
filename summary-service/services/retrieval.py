import os
from supabase import create_client, Client
from functools import lru_cache

@lru_cache(maxsize=1)
def get_supabase() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY")
    if not url or not key:
        raise RuntimeError("Supabase env vars missing")
    return create_client(url, key)

def retrieve_chunks(
    embedding: list[float],
    count: int = 3,
    filter_layer: int | None = None
) -> list[dict]:
    client = get_supabase()
    result = client.rpc("match_chunks", {
        "query_embedding": embedding,
        "match_count": count,
        "filter_layer": filter_layer,
    }).execute()
    return result.data if result.data else []