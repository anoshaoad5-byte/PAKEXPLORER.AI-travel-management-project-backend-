from flask import Blueprint, jsonify, request
from models.hotel import Hotel
from database import db

hotel_bp = Blueprint('hotel_bp', __name__)


# GET all hotels — supports optional ?location= filter, matches name OR location
@hotel_bp.route('/api/hotels', methods=['GET'])
def get_hotels():
    location = request.args.get('location')
    query = Hotel.query
    if location:
        search = f"%{location}%"
        query = query.filter(
            db.or_(
                Hotel.location.ilike(search),
                Hotel.name.ilike(search)
            )
        )
    hotels = query.all()
    return jsonify([hotel.to_dict() for hotel in hotels]), 200


# GET single hotel by id
@hotel_bp.route('/api/hotels/<int:hotel_id>', methods=['GET'])
def get_hotel(hotel_id):
    hotel = Hotel.query.get(hotel_id)
    if not hotel:
        return jsonify({"error": "Hotel not found"}), 404
    return jsonify(hotel.to_dict()), 200


# POST create new hotel (protect this with your admin auth decorator once wired up)
@hotel_bp.route('/api/hotels', methods=['POST'])
def create_hotel():
    data = request.get_json()

    required_fields = ["name", "location", "price_per_night"]
    missing = [f for f in required_fields if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    amenities = data.get("amenities")
    if isinstance(amenities, list):
        amenities = ",".join(amenities)

    new_hotel = Hotel(
        name=data["name"],
        location=data["location"],
        address=data.get("address"),
        description=data.get("description"),
        price_per_night=data["price_per_night"],
        rating=data.get("rating", 0.0),
        image_url=data.get("image_url"),
        amenities=amenities,
        rooms_available=data.get("rooms_available", 0),
        contact_number=data.get("contact_number")
    )
    db.session.add(new_hotel)
    db.session.commit()
    return jsonify(new_hotel.to_dict()), 201


# PUT update existing hotel
@hotel_bp.route('/api/hotels/<int:hotel_id>', methods=['PUT'])
def update_hotel(hotel_id):
    hotel = Hotel.query.get(hotel_id)
    if not hotel:
        return jsonify({"error": "Hotel not found"}), 404

    data = request.get_json()
    for field in ["name", "location", "address", "description", "price_per_night",
                  "rating", "image_url", "rooms_available", "contact_number"]:
        if field in data:
            setattr(hotel, field, data[field])

    if "amenities" in data:
        amenities = data["amenities"]
        hotel.amenities = ",".join(amenities) if isinstance(amenities, list) else amenities

    db.session.commit()
    return jsonify(hotel.to_dict()), 200


# DELETE hotel
@hotel_bp.route('/api/hotels/<int:hotel_id>', methods=['DELETE'])
def delete_hotel(hotel_id):
    hotel = Hotel.query.get(hotel_id)
    if not hotel:
        return jsonify({"error": "Hotel not found"}), 404

    db.session.delete(hotel)
    db.session.commit()
    return jsonify({"message": "Hotel deleted successfully"}), 200