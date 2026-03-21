from sentence_transformers import SentenceTransformer
from functools import lru_cache

@lru_cache(maxsize=1)
def get_model():
    print("[embeddings] loading sentence transformer...")
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    print("[embeddings] ready")
    return model

def embed_state(state: dict) -> list[float]:
    model = get_model()
    # build a natural language description of the state for embedding
    text = (
        f"GDP {state.get('gdp')}% inflation {state.get('inf')}% "
        f"unemployment {state.get('unemp')}% debt {state.get('dbt')}% "
        f"mood {state.get('mood')} currency {state.get('cur')} "
        f"innovation {state.get('inn')} spending {state.get('spd')}% "
        f"printing {'yes' if state.get('prt') else 'no'}"
    )
    return model.encode(text).tolist()