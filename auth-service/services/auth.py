import os
from supabase import create_client, Client
from functools import lru_cache

@lru_cache(maxsize=1)
def get_supabase() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY")
    if not url or not key:
        raise RuntimeError("Missing Supabase env vars")
    return create_client(url, key)

def get_supabase_for_auth() -> Client:
    # service role — bypasses email confirmation
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY")
    if not url or not key:
        raise RuntimeError("Missing Supabase env vars")
    return create_client(url, key)