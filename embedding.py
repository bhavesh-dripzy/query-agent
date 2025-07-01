from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
import os

model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.IndexFlatL2(384)
queries, results = [], []

if os.path.exists("cache.json"):
    with open("cache.json", "r") as f:
        try:
            data = json.load(f)
            queries = data.get("queries", [])
            results = data.get("results", [])
            if queries:
                vecs = model.encode(queries)
                index.add(np.array(vecs).astype("float32"))
        except:
            queries, results = [], []

def embed_query(q):
    return model.encode([q])[0].astype("float32")

def search_similar(q, threshold=0.85):
    vec = embed_query(q).reshape(1, -1)
    if len(queries) == 0:
        return None
    D, I = index.search(vec, k=1)
    if D[0][0] < 1 - threshold:
        return results[I[0][0]]
    return None

def add_to_memory(q, summary):
    queries.append(q)
    results.append(summary)
    index.add(embed_query(q).reshape(1, -1))
    with open("cache.json", "w") as f:
        json.dump({"queries": queries, "results": results}, f)
