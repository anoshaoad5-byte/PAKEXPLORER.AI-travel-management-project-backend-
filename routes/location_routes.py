from flask import Blueprint, request, jsonify
from database import db
from models.user_location import UserLocation
from models.destination import Destination
from utils.auth_utils import token_required
import math

location_bp = Blueprint("location", __name__)


def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


@location_bp.route("/location/update", methods=["POST"])
@token_required
def update_location():
    data = request.get_json()

    latitude = data.get("latitude")
    longitude = data.get("longitude")

    if latitude is None or longitude is None:
        return jsonify({"error": "latitude and longitude are required"}), 400

    existing = UserLocation.query.filter_by(user_id=request.user_id).first()

    if existing:
        existing.latitude = latitude
        existing.longitude = longitude
    else:
        existing = UserLocation(
            user_id=request.user_id,
            latitude=latitude,
            longitude=longitude
        )
        db.session.add(existing)

    db.session.commit()

    return jsonify({"message": "Location updated"}), 200


@location_bp.route("/location/nearby", methods=["GET"])
@token_required
def nearby_destinations():
    user_location = UserLocation.query.filter_by(user_id=request.user_id).first()

    if not user_location:
        return jsonify({"error": "No location set for this user yet"}), 404

    destinations = Destination.query.filter(
        Destination.latitude.isnot(None),
        Destination.longitude.isnot(None)
    ).all()

    results = []
    for d in destinations:
        distance_km = haversine_distance(
            user_location.latitude, user_location.longitude,
            d.latitude, d.longitude
        )
        results.append({
            "id": d.id,
            "name": d.name,
            "city": d.city,
            "province": d.province,
            "distance_km": round(distance_km, 2)
        })

    results.sort(key=lambda x: x["distance_km"])

    return jsonify(results), 200