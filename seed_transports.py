"""
Run this once to populate the transports table with sample data.
Place in backend/ next to app.py, then run: python seed_transports.py
"""

from app import app
from database import db
from models.transport import Transport

transports_data = [
    {
        "provider_name": "Daewoo Express",
        "type": "Bus",
        "from_city": "Lahore",
        "to_city": "Islamabad",
        "departure_time": "08:00 AM",
        "arrival_time": "12:30 PM",
        "price": 2200,
        "rating": 4.3,
        "image_url": "https://picsum.photos/seed/daewoo1/400/250",
        "amenities": "AC,WiFi,Snacks,Reclining Seats",
        "seats_available": 25,
        "contact_number": "+92-42-111-007-008"
    },
    {
        "provider_name": "PIA Domestic",
        "type": "Flight",
        "from_city": "Karachi",
        "to_city": "Lahore",
        "departure_time": "10:15 AM",
        "arrival_time": "12:00 PM",
        "price": 18000,
        "rating": 3.9,
        "image_url": "https://picsum.photos/seed/pia1/400/250",
        "amenities": "In-flight Meal,Baggage Included",
        "seats_available": 40,
        "contact_number": "+92-21-111-786-786"
    },
    {
        "provider_name": "Pakistan Railways - Green Line",
        "type": "Train",
        "from_city": "Karachi",
        "to_city": "Rawalpindi",
        "departure_time": "06:00 PM",
        "arrival_time": "01:00 PM (next day)",
        "price": 3500,
        "rating": 4.1,
        "image_url": "https://picsum.photos/seed/greenline1/400/250",
        "amenities": "AC,Dining Car,Sleeper Berths",
        "seats_available": 60,
        "contact_number": "+92-21-111-000-111"
    },
    {
        "provider_name": "Careem Rent-a-Car",
        "type": "Car Rental",
        "from_city": "Islamabad",
        "to_city": "Hunza",
        "departure_time": "Flexible",
        "arrival_time": "Flexible",
        "price": 15000,
        "rating": 4.4,
        "image_url": "https://picsum.photos/seed/careemcar1/400/250",
        "amenities": "AC,Driver Included,4x4 Available",
        "seats_available": 5,
        "contact_number": "+92-300-1234567"
    },
    {
        "provider_name": "Faisal Movers",
        "type": "Bus",
        "from_city": "Peshawar",
        "to_city": "Quetta",
        "departure_time": "07:30 AM",
        "arrival_time": "08:00 PM",
        "price": 4200,
        "rating": 4.0,
        "image_url": "https://picsum.photos/seed/faisalmovers1/400/250",
        "amenities": "AC,WiFi,Charging Ports",
        "seats_available": 30,
        "contact_number": "+92-91-111-332-332"
    },
    {
        "provider_name": "Airblue",
        "type": "Flight",
        "from_city": "Islamabad",
        "to_city": "Gilgit",
        "departure_time": "07:00 AM",
        "arrival_time": "08:00 AM",
        "price": 22000,
        "rating": 4.2,
        "image_url": "https://picsum.photos/seed/airblue1/400/250",
        "amenities": "Scenic Route,In-flight Snack",
        "seats_available": 20,
        "contact_number": "+92-21-111-247-258"
    },
    {
        "provider_name": "Skyways",
        "type": "Bus",
        "from_city": "Karachi",
        "to_city": "Hyderabad",
        "departure_time": "09:00 AM",
        "arrival_time": "11:30 AM",
        "price": 1200,
        "rating": 3.8,
        "image_url": "https://picsum.photos/seed/skyways1/400/250",
        "amenities": "AC,WiFi",
        "seats_available": 35,
        "contact_number": "+92-21-111-759-929"
    },
]

with app.app_context():
    added = 0
    for data in transports_data:
        exists = Transport.query.filter_by(
            provider_name=data["provider_name"],
            from_city=data["from_city"],
            to_city=data["to_city"]
        ).first()
        if not exists:
            t = Transport(**data)
            db.session.add(t)
            added += 1
    db.session.commit()
    print(f"Seeded {added} new transport options (skipped duplicates).")