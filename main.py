from fastapi import FastAPI
from pydantic import BaseModel
from llm_utils import is_valid_query, summarize_text
from embedding import search_similar, add_to_memory
from scraper import scrape_serpapi  # 👈 Direct import, no subprocess

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
def handle_query(data: QueryRequest):
    q = data.query.strip()

    # Step 1: Validate the query
    if not is_valid_query(q):
        return {"valid": False, "message": "This is not a valid query."}

    # Step 2: Check similarity cache
    cached = search_similar(q)
    if cached:
        return {"valid": True, "cached": True, "summary": cached}

    # Step 3: Scrape using SerpAPI
    links = scrape_serpapi(q)
    if not links or "error" in links[0]:
        return {"valid": False, "error": links[0].get("error", "Unknown error")}

    # Step 4: Combine and summarize
    combined = "\n\n".join([f"{link['title']}: {link['url']}" for link in links])
    summary = summarize_text(combined)

    # Step 5: Save to memory/cache
    add_to_memory(q, summary)

    return {"valid": True, "cached": False, "summary": summary}
