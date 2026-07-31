"""
Seed script for PakExplorer AI - Travel Packages
Run this once to populate the packages table with realistic data.

Usage (from backend/ folder, with conda env activated):
    python seed_packages.py
"""

import json
from app import app
from database import db
from models.package import Package

packages_data = [
    {
        "title": "Hunza Family Explorer",
        "type": "Family",
        "destination": "Hunza",
        "duration_days": 5,
        "price_per_person": 32000,
        "group_size": "2-6 people",
        "image": "hunza-family.jpg",
        "images": json.dumps(["hunza-family-1.jpg", "hunza-family-2.jpg", "hunza-family-3.jpg"]),
        "short_description": "A comfortable, family-friendly journey through the Hunza Valley featuring scenic viewpoints, easy walks, and kid-safe hotels.",
        "inclusions": json.dumps([
            "4-star family hotel stay",
            "Private AC transport",
            "Daily breakfast & dinner",
            "Local guide",
            "All toll & entry fees"
        ]),
        "itinerary_summary": json.dumps([
            "Day 1: Arrival in Hunza, hotel check-in, evening at Karimabad bazaar",
            "Day 2: Baltit Fort visit, Duikar viewpoint sunset",
            "Day 3: Attabad Lake boating, Passu Cones photo stop",
            "Day 4: Altit Fort, local orchard walk, family time",
            "Day 5: Departure"
        ]),
        "rating": 4.7
    },
    {
        "title": "Naran Family Getaway",
        "type": "Family",
        "destination": "Naran, Kaghan",
        "duration_days": 4,
        "price_per_person": 22000,
        "group_size": "2-8 people",
        "image": "naran-family.jpg",
        "images": json.dumps(["naran-family-1.jpg", "naran-family-2.jpg"]),
        "short_description": "Easy-paced trip to Naran and Kaghan Valley, ideal for families with children, with comfortable stays and short jeep excursions.",
        "inclusions": json.dumps([
            "3-star hotel stay",
            "Private transport",
            "Daily breakfast",
            "Saif-ul-Malook jeep ride",
            "Local guide"
        ]),
        "itinerary_summary": json.dumps([
            "Day 1: Arrival in Naran, leisure evening",
            "Day 2: Lake Saif-ul-Malook jeep trip",
            "Day 3: Kaghan Valley sightseeing, local markets",
            "Day 4: Departure"
        ]),
        "rating": 4.4
    },
    {
        "title": "Hunza Honeymoon Retreat",
        "type": "Honeymoon",
        "destination": "Hunza",
        "duration_days": 6,
        "price_per_person": 65000,
        "group_size": "2 people",
        "image": "hunza-honeymoon.jpg",
        "images": json.dumps(["hunza-honeymoon-1.jpg", "hunza-honeymoon-2.jpg", "hunza-honeymoon-3.jpg"]),
        "short_description": "A romantic escape into the Hunza Valley with private mountain-view stays, candlelight dinners, and scenic couple photography stops.",
        "inclusions": json.dumps([
            "5-star luxury hotel with valley view",
            "Private vehicle throughout",
            "Candlelight dinner (1 night)",
            "Couple photography session",
            "All meals included"
        ]),
        "itinerary_summary": json.dumps([
            "Day 1: Arrival, private valley-view suite check-in",
            "Day 2: Eagle's Nest sunrise viewpoint, Karimabad exploration",
            "Day 3: Attabad Lake private boat ride",
            "Day 4: Passu Cones & Hussaini Suspension Bridge",
            "Day 5: Leisure day, candlelight dinner",
            "Day 6: Departure"
        ]),
        "rating": 4.9
    },
    {
        "title": "Fairy Meadows Honeymoon Escape",
        "type": "Honeymoon",
        "destination": "Fairy Meadows",
        "duration_days": 4,
        "price_per_person": 55000,
        "group_size": "2 people",
        "image": "fairy-meadows-honeymoon.jpg",
        "images": json.dumps(["fairy-meadows-1.jpg", "fairy-meadows-2.jpg"]),
        "short_description": "An intimate trip to the base of Nanga Parbat, staying in cozy wooden cottages surrounded by pine forests and mountain views.",
        "inclusions": json.dumps([
            "Wooden cottage stay",
            "Jeep transport to Fairy Meadows",
            "All meals included",
            "Bonfire evening",
            "Local guide"
        ]),
        "itinerary_summary": json.dumps([
            "Day 1: Drive to Raikot Bridge, jeep to Fairy Meadows",
            "Day 2: Nanga Parbat base camp trek",
            "Day 3: Leisure day, bonfire evening",
            "Day 4: Departure"
        ]),
        "rating": 4.8
    },
    {
        "title": "Skardu Adventure Trek",
        "type": "Adventure",
        "destination": "Skardu",
        "duration_days": 7,
        "price_per_person": 48000,
        "group_size": "4-10 people",
        "image": "skardu-adventure.jpg",
        "images": json.dumps(["skardu-adventure-1.jpg", "skardu-adventure-2.jpg", "skardu-adventure-3.jpg"]),
        "short_description": "A rugged adventure through Skardu's dramatic landscapes, including Deosai Plains, Shangrila Lake, and jeep tracks through the Karakoram.",
        "inclusions": json.dumps([
            "Guesthouse & camping stays",
            "4x4 jeep transport",
            "All meals",
            "Professional trekking guide",
            "Camping equipment"
        ]),
        "itinerary_summary": json.dumps([
            "Day 1: Arrival in Skardu, briefing",
            "Day 2: Shangrila Lake & Upper Kachura Lake",
            "Day 3-4: Deosai Plains camping",
            "Day 5: Sheosar Lake trek",
            "Day 6: Skardu Fort & bazaar",
            "Day 7: Departure"
        ]),
        "rating": 4.6
    },
    {
        "title": "Kumrat Valley Adventure",
        "type": "Adventure",
        "destination": "Kumrat Valley",
        "duration_days": 4,
        "price_per_person": 27000,
        "group_size": "4-8 people",
        "image": "kumrat-adventure.jpg",
        "images": json.dumps(["kumrat-adventure-1.jpg", "kumrat-adventure-2.jpg"]),
        "short_description": "Off-the-beaten-path trekking through dense pine forests and river trails in one of Pakistan's most underrated adventure spots.",
        "inclusions": json.dumps([
            "Camping stay",
            "4x4 jeep transport",
            "All meals",
            "Trekking guide",
            "Bonfire nights"
        ]),
        "itinerary_summary": json.dumps([
            "Day 1: Drive to Kumrat, camp setup",
            "Day 2: Katora Lake trek",
            "Day 3: River trail hike, bonfire night",
            "Day 4: Departure"
        ]),
        "rating": 4.5
    },
    {
        "title": "Swat Student Budget Tour",
        "type": "Student",
        "destination": "Swat Valley",
        "duration_days": 3,
        "price_per_person": 9500,
        "group_size": "10-20 people",
        "image": "swat-student.jpg",
        "images": json.dumps(["swat-student-1.jpg", "swat-student-2.jpg"]),
        "short_description": "A budget-friendly group tour designed for university students, covering Swat's top spots with shared accommodation and public transport.",
        "inclusions": json.dumps([
            "Hostel-style shared rooms",
            "Coaster bus transport",
            "Breakfast included",
            "Group guide"
        ]),
        "itinerary_summary": json.dumps([
            "Day 1: Departure & arrival in Mingora, Fizagat Park",
            "Day 2: Malam Jabba, Marghazar Green Chalet",
            "Day 3: Bahrain river point, return journey"
        ]),
        "rating": 4.2
    },
    {
        "title": "Nathiagali Student Trip",
        "type": "Student",
        "destination": "Nathiagali",
        "duration_days": 2,
        "price_per_person": 6000,
        "group_size": "10-25 people",
        "image": "nathiagali-student.jpg",
        "images": json.dumps(["nathiagali-student-1.jpg"]),
        "short_description": "A short, affordable weekend trip perfect for student groups, featuring pine forest walks and viewpoint hikes.",
        "inclusions": json.dumps([
            "Shared guesthouse stay",
            "Bus transport",
            "Breakfast included"
        ]),
        "itinerary_summary": json.dumps([
            "Day 1: Departure, arrival, Mall Road walk",
            "Day 2: Miranjani Top hike, return journey"
        ]),
        "rating": 4.0
    },
    {
        "title": "Hunza Luxury Signature Tour",
        "type": "Luxury",
        "destination": "Hunza",
        "duration_days": 5,
        "price_per_person": 95000,
        "group_size": "2-4 people",
        "image": "hunza-luxury.jpg",
        "images": json.dumps(["hunza-luxury-1.jpg", "hunza-luxury-2.jpg"]),
        "short_description": "A premium travel experience with 5-star stays, private guided tours, and curated dining across Hunza's most scenic locations.",
        "inclusions": json.dumps([
            "5-star hotel (Serena-level)",
            "Private luxury vehicle",
            "All meals at premium restaurants",
            "Dedicated private guide",
            "Priority sightseeing access"
        ]),
        "itinerary_summary": json.dumps([
            "Day 1: Arrival, luxury suite check-in",
            "Day 2: Private Eagle's Nest sunrise tour",
            "Day 3: Attabad Lake private excursion",
            "Day 4: Karimabad heritage tour, fine dining",
            "Day 5: Departure"
        ]),
        "rating": 4.9
    },
    {
        "title": "Swat Budget Explorer",
        "type": "Budget",
        "destination": "Swat Valley",
        "duration_days": 3,
        "price_per_person": 8000,
        "group_size": "2-6 people",
        "image": "swat-budget.jpg",
        "images": json.dumps(["swat-budget-1.jpg"]),
        "short_description": "An affordable way to experience Swat Valley's best spots using public transport and guesthouse stays, ideal for budget travelers.",
        "inclusions": json.dumps([
            "Guesthouse stay",
            "Public van transport",
            "Breakfast included"
        ]),
        "itinerary_summary": json.dumps([
            "Day 1: Arrival in Mingora, local market visit",
            "Day 2: Malam Jabba day trip",
            "Day 3: Fizagat Park, return journey"
        ]),
        "rating": 4.1
    }
]

def seed():
    with app.app_context():
        existing = Package.query.count()
        if existing > 0:
            print(f"Packages table already has {existing} records. Skipping seed to avoid duplicates.")
            print("If you want to re-seed, delete existing packages first.")
            return

        for data in packages_data:
            package = Package(**data)
            db.session.add(package)

        db.session.commit()
        print(f"Successfully seeded {len(packages_data)} packages!")

if __name__ == "__main__":
    seed()