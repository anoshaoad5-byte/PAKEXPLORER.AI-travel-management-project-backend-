from app import app
from database import db
from models.destination import Destination
from services.image_service import fetch_destination_image
import time

# Simplified, broader search terms for destinations that had no Unsplash match
RETRY_QUERIES = {
    "Murree Hills": "Murree Pakistan hill station",
    "Kalash Valley": "Kalash people Chitral",
    "Ranikot Fort": "Ranikot Fort Sindh",
    "Shandur Pass": "Shandur polo ground",
    "Lahore Walled City": "Lahore old city bazaar",
    "Gorakh Hill Station": "Gorakh Hill Sindh",
    "Chitral Valley": "Chitral Pakistan mountains",
    "Makli Necropolis": "Makli tombs Thatta",
    "Katas Raj Temples": "Katas Raj temple pond",
    "Clifton Beach": "Karachi beach",
    "Astola Island": "Astola Island Balochistan",
    "Cholistan Desert": "Cholistan desert Pakistan",
    "Multan Old City": "Multan shrine Pakistan"
}

with app.app_context():
    for name, query in RETRY_QUERIES.items():
        d = Destination.query.filter_by(name=name).first()
        if not d:
            print(f"Skipping {name} — not found in DB")
            continue

        print(f"Retrying: {name} (query: '{query}') ...")
        image_url = fetch_destination_image(query)

        if image_url:
            d.image = image_url
            db.session.commit()
            print(f"  -> Updated")
        else:
            print(f"  -> Still no image found")

        time.sleep(1.5)

    print("Retry complete.")