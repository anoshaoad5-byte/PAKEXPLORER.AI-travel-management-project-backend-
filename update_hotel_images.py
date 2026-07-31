"""
Run this after placing your real hotel photos in backend/static/hotel_images/
"""

from app import app
from database import db
from models.hotel import Hotel

image_map = {
    "Pearl Continental Lahore": "pearl_continental_lahore.jpg",
    "Avari Lahore": "avari_lahore.jpg",
    "Pearl Continental Karachi": "pearl_continental_karachi.jpg",
    "Avari Towers Karachi": "avari_towers_karachi.jpg",
    "Pearl Continental Peshawar": "pearl_continental_peshawar.jpg",
    "Shelton's Rezidor Peshawar": "sheltons_peshawar.jpg",
    "Serena Hotel Quetta": "serena_quetta.jpg",
    "Bloom Star Hotel Quetta": "bloom_star_quetta.jpg",
    "Serena Hunza": "serena_hunza.jpg",
    "Hunza Embassy Hotel": "hunza_embassy.jpg",
}

BASE_URL = "http://127.0.0.1:5000/static/hotel_images"

with app.app_context():
    updated = 0
    not_found = []
    for name, filename in image_map.items():
        hotel = Hotel.query.filter_by(name=name).first()
        if hotel:
            hotel.image_url = f"{BASE_URL}/{filename}"
            updated += 1
        else:
            not_found.append(name)

    db.session.commit()
    print(f"Updated {updated} hotel images.")
    if not_found:
        print("Could not find these hotels in the database:", not_found)