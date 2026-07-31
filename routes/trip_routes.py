from flask import Blueprint, request, jsonify
from database import db
from models.trip import Trip
from utils.auth_utils import token_required

trip_bp = Blueprint("trip", __name__, url_prefix="/api")


@trip_bp.route("/trips", methods=["GET"])
@token_required
def get_my_trips():
    trips = Trip.query.filter_by(user_id=request.user_id).all()
    result = []
    for t in trips:
        result.append({
            "id": t.id,
            "destination_id": t.destination_id,
            "start_date": str(t.start_date) if t.start_date else None,
            "end_date": str(t.end_date) if t.end_date else None,
            "total_budget": t.total_budget,
            "status": t.status
        })
    return jsonify(result), 200


@trip_bp.route("/trips", methods=["POST"])
@token_required
def create_trip():
    data = request.get_json()

    destination_id = data.get("destination_id")
    if not destination_id:
        return jsonify({"error": "destination_id is required"}), 400

    new_trip = Trip(
        user_id=request.user_id,
        destination_id=destination_id,
        start_date=data.get("start_date"),
        end_date=data.get("end_date"),
        total_budget=data.get("total_budget"),
        status=data.get("status", "Planned")
    )

    db.session.add(new_trip)
    db.session.commit()

    return jsonify({"message": "Trip created", "id": new_trip.id}), 201


@trip_bp.route("/trips/<int:trip_id>", methods=["PUT"])
@token_required
def update_trip(trip_id):
    trip = Trip.query.get(trip_id)
    if not trip or trip.user_id != request.user_id:
        return jsonify({"error": "Trip not found"}), 404

    data = request.get_json()

    trip.start_date = data.get("start_date", trip.start_date)
    trip.end_date = data.get("end_date", trip.end_date)
    trip.total_budget = data.get("total_budget", trip.total_budget)
    trip.status = data.get("status", trip.status)

    db.session.commit()

    return jsonify({"message": "Trip updated"}), 200


@trip_bp.route("/trips/<int:trip_id>", methods=["DELETE"])
@token_required
def delete_trip(trip_id):
    trip = Trip.query.get(trip_id)
    if not trip or trip.user_id != request.user_id:
        return jsonify({"error": "Trip not found"}), 404

    db.session.delete(trip)
    db.session.commit()

    return jsonify({"message": "Trip deleted"}), 200