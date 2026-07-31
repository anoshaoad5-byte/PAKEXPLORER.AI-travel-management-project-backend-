from flask import Blueprint, jsonify, request
from models.hotel import Hotel
from models.destination import Destination
from models.transport import Transport
import math

budget_bp = Blueprint('budget_bp', __name__)


@budget_bp.route('/api/budget/calculate', methods=['POST'])
def calculate_budget():
    data = request.get_json()

    members = data.get('members')
    if not members or int(members) < 1:
        return jsonify({"error": "members must be a positive integer"}), 400
    members = int(members)

    nights = data.get('nights', 1)
    try:
        nights = max(1, int(nights))
    except (TypeError, ValueError):
        nights = 1

    breakdown = []
    total = 0.0

    # --- Hotel ---
    hotel_id = data.get('hotel_id')
    if hotel_id:
        hotel = Hotel.query.get(hotel_id)
        if not hotel:
            return jsonify({"error": f"Hotel {hotel_id} not found"}), 404
        rooms_needed = math.ceil(members / 2)
        hotel_cost = hotel.price_per_night * nights * rooms_needed
        breakdown.append({
            "category": "Hotel",
            "label": f"{hotel.name} ({rooms_needed} room(s) x {nights} night(s))",
            "amount": round(hotel_cost, 2)
        })
        total += hotel_cost

    # --- Transportation ---
    transport_id = data.get('transport_id')
    if transport_id:
        transport = Transport.query.get(transport_id)
        if not transport:
            return jsonify({"error": f"Transport {transport_id} not found"}), 404
        transport_cost = transport.price * members
        breakdown.append({
            "category": "Transportation",
            "label": f"{transport.provider_name} ({transport.from_city} → {transport.to_city}) x {members} member(s)",
            "amount": round(transport_cost, 2)
        })
        total += transport_cost

    # --- Destination / place ---
    destination_id = data.get('destination_id')
    if destination_id:
        destination = Destination.query.get(destination_id)
        if not destination:
            return jsonify({"error": f"Destination {destination_id} not found"}), 404
        if destination.budget:
            dest_cost = destination.budget * members
            breakdown.append({
                "category": "Place",
                "label": f"{destination.name} (est. cost x {members} member(s))",
                "amount": round(dest_cost, 2)
            })
            total += dest_cost

    # --- Custom items (shopping, dinner, breakfast, lunch, etc.) ---
    custom_items = data.get('custom_items', [])
    if isinstance(custom_items, list):
        for item in custom_items:
            name = item.get('name')
            amount = item.get('amount')
            if not name or amount is None:
                continue
            try:
                amount = float(amount)
            except (TypeError, ValueError):
                continue
            breakdown.append({
                "category": "Custom",
                "label": name,
                "amount": round(amount, 2)
            })
            total += amount

    return jsonify({
        "members": members,
        "nights": nights,
        "breakdown": breakdown,
        "total": round(total, 2),
        "per_person": round(total / members, 2)
    }), 200