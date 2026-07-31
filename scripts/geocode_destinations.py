import sys
import os
import time
import requests

# Allow importing from the backend root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from database import db
from models.destination import Destination

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
HEADERS = {
    "User-Agent": "PakExplorerAI/1.0 (student project; contact: your-email@example.com)"
}


def geocode(query):
    params = {
        "q": query,
        "format": "json",
        "limit": 1,
        "countrycodes": "pk"
    }
    response = requests.get(NOMINATIM_URL, params=params, headers=HEADERS, timeout=10)
    response.raise_for_status()
    results = response.json()
    if not results:
        return None
    return float(results[0]["lat"]), float(results[0]["lon"])


def main():
    with app.app_context():
        missing = Destination.query.filter(
            (Destination.latitude.is_(None)) | (Destination.longitude.is_(None))
        ).all()

        if not missing:
            print("All destinations already have coordinates. Nothing to do.")
            return

        print(f"Found {len(missing)} destination(s) missing coordinates.\n")

        updated = 0
        failed = []

        for dest in missing:
            # Build the most specific query we can from available fields
            parts = [dest.name]
            if dest.city:
                parts.append(dest.city)
            if dest.province:
                parts.append(dest.province)
            parts.append("Pakistan")
            query = ", ".join(parts)

            print(f"Geocoding: {query} ...", end=" ")

            try:
                result = geocode(query)
                if result:
                    lat, lon = result
                    dest.latitude = lat
                    dest.longitude = lon
                    db.session.commit()
                    updated += 1
                    print(f"OK ({lat}, {lon})")
                else:
                    failed.append(dest.name)
                    print("NOT FOUND")
            except Exception as e:
                failed.append(dest.name)
                print(f"ERROR: {e}")

            # Respect Nominatim's 1 request/second rate limit
            time.sleep(1.1)

        print(f"\nDone. Updated {updated}/{len(missing)}.")
        if failed:
            print(f"Could not geocode: {', '.join(failed)}")
            print("These may need manual coordinates or a more specific city/province name.")


if __name__ == "__main__":
    main()