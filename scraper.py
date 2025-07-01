import sys
import json
import requests
from requests_toolbelt.adapters import host_header_ssl

def scrape_serpapi(query: str):
    API_KEY = "190df1f29712227bc4fc193621b63955433738dbe2d835afa9b1e8d722016194"

    session = requests.Session()
    session.mount("https://", host_header_ssl.HostHeaderSSLAdapter())

    url = "https://serpapi.com/search"
    headers = {
        "Host": "serpapi.com"
    }
    params = {
        "engine": "google",
        "q": query,
        "api_key": API_KEY
    }

    try:
        res = session.get(url, headers=headers, params=params, timeout=10)
        data = res.json()

        results = []
        for item in data.get("organic_results", [])[:5]:
            results.append({
                "title": item.get("title"),
                "url": item.get("link")
            })

        return results or [{"error": "No results found."}]
    except Exception as e:
        return [{"error": str(e)}]

if __name__ == "__main__":
    query = sys.argv[1]
    print(json.dumps(scrape_serpapi(query), indent=2))
