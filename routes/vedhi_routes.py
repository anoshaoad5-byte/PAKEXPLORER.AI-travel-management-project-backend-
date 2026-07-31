import os
import json
from flask import Blueprint, request, jsonify
from groq import Groq
from models.destination import Destination
from models.package import Package
from models.hotel import Hotel

vedhi_bp = Blueprint("vedhi", __name__)

client = Groq(api_key=os.getenv("GROQ_API_KEY"), timeout=30.0)


def truncate(text, limit=150):
    if not text:
        return ""
    return text[:limit]


def build_context():
    destinations = Destination.query.limit(40).all()
    packages = Package.query.limit(40).all()
    hotels = Hotel.query.limit(40).all()

    destinations_summary = [
        {
            "name": d.name,
            "city": d.city,
            "province": d.province,
            "description": truncate(d.description),
            "famous_places": truncate(d.famous_places),
            "budget": d.budget,
            "best_time_to_visit": d.best_time_to_visit,
        }
        for d in destinations
    ]

    packages_summary = [
        {
            "title": p.title,
            "type": p.type,
            "destination": p.destination,
            "duration_days": p.duration_days,
            "price_per_person": p.price_per_person,
            "short_description": truncate(p.short_description),
        }
        for p in packages
    ]

    hotels_summary = [
        {
            "name": h.name,
            "location": h.location,
            "price_per_night": h.price_per_night,
            "rating": h.rating,
        }
        for h in hotels
    ]

    return {
        "destinations": destinations_summary,
        "packages": packages_summary,
        "hotels": hotels_summary,
    }


@vedhi_bp.route("/api/vedhi/ask", methods=["POST"])
def ask_vedhi():
    data = request.get_json(silent=True) or {}
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "question is required"}), 400

    context = build_context()

    prompt = f"""You are Vedhi, the AI assistant for PakExplorer AI, a travel platform covering all of Pakistan.
Answer using ONLY the data below. If the answer isn't in this data, say you don't have that information.
Keep answers short and specific.

DESTINATIONS:
{json.dumps(context['destinations'])}

PACKAGES:
{json.dumps(context['packages'])}

HOTELS:
{json.dumps(context['hotels'])}

User question: {question}"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
        )
        answer = response.choices[0].message.content.strip()
        return jsonify({"answer": answer}), 200
    except Exception as e:
        print("VEDHI ERROR:", type(e).__name__, str(e))
        return jsonify({"error": f"Could not get an answer: {str(e)}"}), 500