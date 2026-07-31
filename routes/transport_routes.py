from flask import Blueprint, jsonify, request
from models.transport import Transport
from database import db

transport_bp = Blueprint('transport_bp', __name__)


# GET all — supports ?from_city= and ?to_city= and ?type= filters
@transport_bp.route('/api/transports', methods=['GET'])
def get_transports():
    from_city = request.args.get('from_city')
    to_city = request.args.get('to_city')
    ttype = request.args.get('type')

    query = Transport.query
    if from_city:
        query = query.filter(Transport.from_city.ilike(f"%{from_city}%"))
    if to_city:
        query = query.filter(Transport.to_city.ilike(f"%{to_city}%"))
    if ttype:
        query = query.filter(Transport.type.ilike(f"%{ttype}%"))

    results = query.all()
    return jsonify([t.to_dict() for t in results]), 200


@transport_bp.route('/api/transports/cities', methods=['GET'])
def get_transport_cities():
    from_cities = [row[0] for row in db.session.query(Transport.from_city).distinct()]
    to_cities = [row[0] for row in db.session.query(Transport.to_city).distinct()]
    cities = sorted(set(from_cities + to_cities))
    return jsonify(cities), 200


@transport_bp.route('/api/transports/<int:transport_id>', methods=['GET'])
def get_transport(transport_id):
    t = Transport.query.get(transport_id)
    if not t:
        return jsonify({"error": "Transport option not found"}), 404
    return jsonify(t.to_dict()), 200


@transport_bp.route('/api/transports', methods=['POST'])
def create_transport():
    data = request.get_json()
    required = ["provider_name", "type", "from_city", "to_city", "price"]
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    amenities = data.get("amenities")
    if isinstance(amenities, list):
        amenities = ",".join(amenities)

    t = Transport(
        provider_name=data["provider_name"],
        type=data["type"],
        from_city=data["from_city"],
        to_city=data["to_city"],
        departure_time=data.get("departure_time"),
        arrival_time=data.get("arrival_time"),
        price=data["price"],
        rating=data.get("rating", 0.0),
        image_url=data.get("image_url"),
        amenities=amenities,
        seats_available=data.get("seats_available", 0),
        contact_number=data.get("contact_number")
    )
    db.session.add(t)
    db.session.commit()
    return jsonify(t.to_dict()), 201


@transport_bp.route('/api/transports/<int:transport_id>', methods=['PUT'])
def update_transport(transport_id):
    t = Transport.query.get(transport_id)
    if not t:
        return jsonify({"error": "Transport option not found"}), 404

    data = request.get_json()
    for field in ["provider_name", "type", "from_city", "to_city", "departure_time",
                  "arrival_time", "price", "rating", "image_url", "seats_available", "contact_number"]:
        if field in data:
            setattr(t, field, data[field])

    if "amenities" in data:
        amenities = data["amenities"]
        t.amenities = ",".join(amenities) if isinstance(amenities, list) else amenities

    db.session.commit()
    return jsonify(t.to_dict()), 200


@transport_bp.route('/api/transports/<int:transport_id>', methods=['DELETE'])
def delete_transport(transport_id):
    t = Transport.query.get(transport_id)
    if not t:
        return jsonify({"error": "Transport option not found"}), 404
    db.session.delete(t)
    db.session.commit()
    return jsonify({"message": "Transport option deleted successfully"}), 200