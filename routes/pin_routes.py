from flask import Blueprint, jsonify, request
from models.destination import Destination
from models.destination_pin import DestinationPin
from database import db

pin_bp = Blueprint('pin_bp', __name__)


# Public: get a destination's basic map info + all its pins (bazaars/famous places)
@pin_bp.route('/api/destinations/<int:destination_id>/pins', methods=['GET'])
def get_destination_pins(destination_id):
    destination = Destination.query.get(destination_id)
    if not destination:
        return jsonify({"error": "Destination not found"}), 404

    pins = DestinationPin.query.filter_by(destination_id=destination_id).all()

    return jsonify({
        "destination": {
            "id": destination.id,
            "name": destination.name,
            "latitude": destination.latitude,
            "longitude": destination.longitude,
            "image": destination.image
        },
        "pins": [p.to_dict() for p in pins]
    }), 200


# Admin: add a new pin for a destination
@pin_bp.route('/api/destinations/<int:destination_id>/pins', methods=['POST'])
def add_destination_pin(destination_id):
    destination = Destination.query.get(destination_id)
    if not destination:
        return jsonify({"error": "Destination not found"}), 404

    data = request.get_json()
    required = ["name", "latitude", "longitude"]
    missing = [f for f in required if f not in data or data[f] in (None, "")]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    pin = DestinationPin(
        destination_id=destination_id,
        name=data["name"],
        category=data.get("category"),
        latitude=data["latitude"],
        longitude=data["longitude"],
        description=data.get("description"),
        image_url=data.get("image_url"),
        images=data.get("images")  # comma-separated string
    )
    db.session.add(pin)
    db.session.commit()
    return jsonify(pin.to_dict()), 201


# Admin: delete a pin
@pin_bp.route('/api/pins/<int:pin_id>', methods=['DELETE'])
def delete_pin(pin_id):
    pin = DestinationPin.query.get(pin_id)
    if not pin:
        return jsonify({"error": "Pin not found"}), 404
    db.session.delete(pin)
    db.session.commit()
    return jsonify({"deleted": True}), 200