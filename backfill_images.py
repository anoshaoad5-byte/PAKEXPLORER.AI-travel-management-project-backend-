from app import app
from database import db
from models.destination import Destination
from services.image_service import fetch_destination_image
import time

with app.app_context():
    destinations = Destination.query.all()
    print(f"Found {len(destinations)} destinations")

    for d in destinations:
        query = f"{d.name} {d.province} Pakistan"
        print(f"Fetching image for: {d.name} ...")
        image_url = fetch_destination_image(query)

        if image_url:
            d.image = image_url
            db.session.commit()
            print(f"  -> Updated: {image_url}")
        else:
            print(f"  -> No image found, skipping")

        time.sleep(1.5)  # stay safely under 50 requests/hour limit

    print("Backfill complete.")