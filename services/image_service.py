import os
import requests
from dotenv import load_dotenv

load_dotenv()

UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
UNSPLASH_URL = "https://api.unsplash.com/search/photos"


def fetch_destination_image(query):
    """Fetch a real photo URL from Unsplash based on a search query."""
    if not UNSPLASH_ACCESS_KEY:
        print("No Unsplash key found, skipping image fetch")
        return None

    try:
        response = requests.get(
            UNSPLASH_URL,
            params={"query": query, "per_page": 1, "orientation": "landscape"},
            headers={"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"},
            timeout=5
        )
        data = response.json()
        results = data.get("results")
        if results:
            return results[0]["urls"]["regular"]
    except Exception as e:
        print(f"Unsplash fetch failed: {e}")

    return None


def fetch_destination_images(query, count=3):
    """Fetch multiple real photo URLs from Unsplash based on a search query."""
    if not UNSPLASH_ACCESS_KEY:
        print("No Unsplash key found, skipping image fetch")
        return []

    try:
        response = requests.get(
            UNSPLASH_URL,
            params={"query": query, "per_page": count, "orientation": "landscape"},
            headers={"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"},
            timeout=5
        )
        data = response.json()
        results = data.get("results", [])
        return [r["urls"]["regular"] for r in results]
    except Exception as e:
        print(f"Unsplash multi-fetch failed: {e}")

    return []