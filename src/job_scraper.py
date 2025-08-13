import os
from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()

def get_google_jobs(query, location="India", job_type=None):
    params = {
        "engine": "google_jobs",
        "q": query,
        "location": location,
        "api_key": os.getenv("SERPAPI_KEY")
    }

    if job_type:
        params["job_type"] = job_type

    search = GoogleSearch(params)
    results = search.get_dict()
    return results.get("jobs_results", [])
