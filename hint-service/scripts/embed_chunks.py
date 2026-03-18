import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'hint-service'))

from dotenv import load_dotenv
load_dotenv()

from sentence_transformers import SentenceTransformer
from supabase import create_client

# import all layers
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'knowledge'))
from layer1_mechanics import LAYER1
from layer2_pairwise import LAYER2
from layer3_extremes import LAYER3
from layer4_rounds import LAYER4
from layer5_history import LAYER5

ALL_CHUNKS = LAYER1 + LAYER2 + LAYER3 + LAYER4 + LAYER5

def main():
    print(f"[embed] total chunks: {len(ALL_CHUNKS)}")

    supabase = create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_SERVICE_KEY")
    )

    print("[embed] loading embedding model...")
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    print("[embed] model ready")

    success = 0
    errors  = 0

    for chunk in ALL_CHUNKS:
        try:
            embedding = model.encode(
                chunk["content"],
                normalize_embeddings=True
            ).tolist()

            supabase.table("econoquest_chunks").upsert({
                "layer":     chunk["layer"],
                "chunk_key": chunk["chunk_key"],
                "content":   chunk["content"],
                "embedding": embedding,
                "metadata":  chunk.get("metadata", {}),
            }, on_conflict="chunk_key").execute()

            print(f"  ✓ {chunk['chunk_key']}")
            success += 1

        except Exception as e:
            print(f"  ✗ {chunk['chunk_key']}: {e}")
            errors += 1

    print(f"\n[embed] done — {success} success, {errors} errors")

if __name__ == "__main__":
    main()