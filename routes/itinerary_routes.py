import os
import json
from groq import Groq
from flask import Blueprint, request, jsonify
from models.destination import Destination

itinerary_bp = Blueprint("itinerary", __name__)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


@itinerary_bp.route("/api/itinerary/generate", methods=["GET"])
def generate_itinerary():
    destination_id = request.args.get("destination_id", type=int)
    days = request.args.get("days", default=10, type=int)

    if not destination_id:
        return jsonify({"error": "destination_id is required"}), 400

    destination = Destination.query.get(destination_id)
    if not destination:
        return jsonify({"error": "Destination not found"}), 404

    prompt = f"""
You are Vedhi, a Pakistan travel planning assistant. Create a detailed {days}-day
travel itinerary for a trip to {destination.name}, {destination.city}, {destination.province}, Pakistan.

Destination info to use:
- Description: {destination.description or "N/A"}
- Famous places: {destination.famous_places or "N/A"}
- Famous dish: {destination.famous_dish or "N/A"}
- Festivals: {destination.festivals or "N/A"}
- Best time to visit: {destination.best_time_to_visit or "N/A"}

Return ONLY valid JSON (no markdown, no backticks, no extra text) in this exact structure:
{{
  "destination": "{destination.name}",
  "days": [
    {{
      "day": 1,
      "title": "Short title for the day",
      "morning": "What to do in the morning",
      "afternoon": "What to do in the afternoon",
      "evening": "What to do in the evening",
      "tip": "One practical tip for this day"
    }}
  ]
}}

Generate exactly {days} day objects, each with realistic, specific activities based on the
destination info above. Do not repeat the same activities across days.
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        raw_text = response.choices[0].message.content.strip()
        if raw_text.startswith("```"):
            raw_text = raw_text.strip("`")
            if raw_text.startswith("json"):
                raw_text = raw_text[4:].strip()

        itinerary = json.loads(raw_text)
        return jsonify(itinerary), 200

    except json.JSONDecodeError:
        return jsonify({"error": "AI returned an unexpected format. Please try again."}), 502
    except Exception as e:
        return jsonify({"error": f"Could not generate itinerary: {str(e)}"}), 500