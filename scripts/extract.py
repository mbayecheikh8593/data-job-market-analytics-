import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

APP_ID  = os.getenv("ADZUNA_APP_ID")
API_KEY = os.getenv("ADZUNA_API_KEY")

BASE_URL = "https://api.adzuna.com/v1/api/jobs/fr/search"

KEYWORDS = ["data engineer", "data analyst", "data scientist"]

def fetch_jobs(keyword, max_pages=3):
    results = []
    for page in range(1, max_pages + 1):
        url = f"{BASE_URL}/{page}"
        params = {
            "app_id": APP_ID,
            "app_key": API_KEY,
            "results_per_page": 50,
            "what": keyword,
            "content-type": "application/json"
        }
        r = requests.get(url, params=params)
        if r.status_code != 200:
            print(f"Erreur {r.status_code} pour '{keyword}' page {page}")
            break
        data = r.json().get("results", [])
        if not data:
            break
        results.extend(data)
        print(f"  '{keyword}' — page {page} : {len(data)} offres récupérées")
    return results

if __name__ == "__main__":
    all_jobs = []
    for kw in KEYWORDS:
        print(f"\nExtraction : {kw}")
        all_jobs.extend(fetch_jobs(kw))

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"data/raw/adzuna_{ts}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(all_jobs, f, ensure_ascii=False, indent=2)

    print(f"\n✓ {len(all_jobs)} offres sauvegardées dans {path}")