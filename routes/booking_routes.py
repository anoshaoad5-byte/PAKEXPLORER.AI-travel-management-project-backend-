from flask import Blueprint, jsonify, request
from models.booking import Booking
from models.destination import Destination
from models.hotel import Hotel
from models.transport import Transport
from models.package import Package
from services.email_service import send_booking_confirmation, send_ticket_email
from database import db

booking_bp = Blueprint('booking_bp', __name__)


@booking_bp.route('/api/bookings', methods=['POST'])
def create_booking():
    data = request.get_json()
    required = ["full_name", "email", "members"]
    missing = [f for f in required if f not in data or not data[f]]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    booking = Booking(
        full_name=data["full_name"],
        email=data["email"],
        phone=data.get("phone"),
        destination_id=data.get("destination_id"),
        hotel_id=data.get("hotel_id"),
        transport_id=data.get("transport_id"),
        package_id=data.get("package_id"),
        members=data["members"],
        travel_date=data.get("travel_date"),
        nights=data.get("nights"),
        notes=data.get("notes"),
        payment_method=data.get("payment_method"),
        total_amount=data.get("total_amount"),
        status="pending"
    )
    db.session.add(booking)
    db.session.commit()
    return jsonify(booking.to_dict()), 201


# Admin: view all bookings, optionally filter by status
@booking_bp.route('/api/bookings', methods=['GET'])
def get_bookings():
    status = request.args.get('status')
    query = Booking.query
    if status:
        query = query.filter(Booking.status == status)
    bookings = query.order_by(Booking.created_at.desc()).all()
    return jsonify([b.to_dict() for b in bookings]), 200


# Admin: approve a booking -> triggers confirmation email
@booking_bp.route('/api/bookings/<int:booking_id>/approve', methods=['PUT'])
def approve_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    booking.status = "approved"
    db.session.commit()

    destination = Destination.query.get(booking.destination_id) if booking.destination_id else None
    hotel = Hotel.query.get(booking.hotel_id) if booking.hotel_id else None
    transport = Transport.query.get(booking.transport_id) if booking.transport_id else None

    email_sent = send_booking_confirmation(
        booking,
        destination_name=destination.name if destination else None,
        hotel_name=hotel.name if hotel else None,
        transport_name=transport.provider_name if transport else None
    )

    return jsonify({"booking": booking.to_dict(), "email_sent": email_sent}), 200


# Admin: reject a booking
@booking_bp.route('/api/bookings/<int:booking_id>/reject', methods=['PUT'])
def reject_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({"error": "Booking not found"}), 404
    booking.status = "rejected"
    db.session.commit()
    return jsonify(booking.to_dict()), 200


@booking_bp.route('/api/bookings/<int:booking_id>/cancel', methods=['PUT'])
def cancel_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    data = request.get_json() or {}
    booking.status = "cancelled"
    booking.refund_percentage = data.get("refund_percentage")
    db.session.commit()

    return jsonify(booking.to_dict()), 200


# User: send/re-send the ticket + destination checklist to their own email
# (used by the "Save & Email" button on the User Dashboard, approved bookings only)
@booking_bp.route('/api/bookings/<int:booking_id>/send-ticket', methods=['POST'])
def send_ticket(booking_id):
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    if booking.status != "approved":
        return jsonify({"error": "Only approved bookings have a ticket to send"}), 400

    destination = Destination.query.get(booking.destination_id) if booking.destination_id else None
    hotel = Hotel.query.get(booking.hotel_id) if booking.hotel_id else None
    transport = Transport.query.get(booking.transport_id) if booking.transport_id else None
    package = Package.query.get(booking.package_id) if booking.package_id else None

    inclusions = None
    if package and package.inclusions:
        try:
            import json
            inclusions = json.loads(package.inclusions)
        except Exception:
            inclusions = None

    email_sent = send_ticket_email(
        booking,
        destination=destination,
        hotel_name=hotel.name if hotel else None,
        transport_name=transport.provider_name if transport else None,
        package_name=package.title if package else None,
        inclusions=inclusions
    )

    return jsonify({"email_sent": email_sent}), 200