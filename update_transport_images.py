"""
Run this after placing your real transport photos in backend/static/transport_images/
Place this file in backend/ next to app.py, then run: python update_transport_images.py
"""

from app import app
from database import db
from models.transport import Transport

image_map = {
    "Daewoo Express": "daewoo_express.jpg",
    "PIA Domestic": "pia_domestic.jpg",
    "Pakistan Railways - Green Line": "green_line.jpg",
    "Careem Rent-a-Car": "careem_rental.jpg",
    "Faisal Movers": "faisal_movers.jpg",
    "Airblue": "airblue.jpg",
    "Skyways": "skyways.jpg",
}

BASE_URL = "http://127.0.0.1:5000/static/transport_images"

with app.app_context():
    updated = 0
    not_found = []
    for name, filename in image_map.items():
        t = Transport.query.filter_by(provider_name=name).first()
        if t:
            t.image_url = f"{BASE_URL}/{filename}"
            updated += 1
        else:
            not_found.append(name)

    db.session.commit()
    print(f"Updated {updated} transport images.")
    if not_found:
        print("Could not find these providers in the database:", not_found)