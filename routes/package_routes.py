from flask import Blueprint, jsonify, request
from models.package import Package
from database import db

package_bp = Blueprint("package_bp", __name__)


def package_to_dict(p):
    return {
        "id": p.id,
        "title": p.title,
        "type": p.type,
        "destination": p.destination,
        "duration_days": p.duration_days,
        "price_per_person": p.price_per_person,
        "group_size": p.group_size,
        "image": p.image,
        "images": p.images,
        "short_description": p.short_description,
        "inclusions": p.inclusions,
        "itinerary_summary": p.itinerary_summary,
        "rating": p.rating,
        "itinerary_days": p.itinerary_days,
        "available_days": p.available_days,
        "contact_number": p.contact_number,
        "vibe_tagline": p.vibe_tagline
    }


@package_bp.route("/api/packages", methods=["GET"])
def get_packages():
    package_type = request.args.get("type")
    destination = request.args.get("destination")

    query = Package.query

    if package_type:
        query = query.filter_by(type=package_type)
    if destination:
        query = query.filter(Package.destination.ilike(f"%{destination}%"))

    packages = query.all()
    return jsonify([package_to_dict(p) for p in packages])


@package_bp.route("/api/packages/<int:package_id>", methods=["GET"])
def get_package_detail(package_id):
    p = Package.query.get_or_404(package_id)
    return jsonify(package_to_dict(p))


@package_bp.route("/api/packages", methods=["POST"])
def create_package():
    data = request.get_json()

    required_fields = ["title", "type", "destination", "duration_days", "price_per_person", "short_description"]
    missing = [f for f in required_fields if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    new_package = Package(
        title=data.get("title"),
        type=data.get("type"),
        destination=data.get("destination"),
        duration_days=data.get("duration_days"),
        price_per_person=data.get("price_per_person"),
        group_size=data.get("group_size"),
        image=data.get("image"),
        images=data.get("images"),
        short_description=data.get("short_description"),
        inclusions=data.get("inclusions"),
        itinerary_summary=data.get("itinerary_summary"),
        rating=data.get("rating"),
        itinerary_days=data.get("itinerary_days"),
        available_days=data.get("available_days"),
        contact_number=data.get("contact_number"),
        vibe_tagline=data.get("vibe_tagline")
    )

    db.session.add(new_package)
    db.session.commit()

    return jsonify(package_to_dict(new_package)), 201