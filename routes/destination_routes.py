from flask import Blueprint, request, jsonify
from database import db
from models.destination import Destination
import json

destination_bp = Blueprint("destination", __name__, url_prefix="/api")


def destination_to_dict(d):
    try:
        images_list = json.loads(d.images) if d.images else []
    except (json.JSONDecodeError, TypeError):
        images_list = []

    return {
        "id": d.id,
        "name": d.name,
        "province": d.province,
        "city": d.city,
        "description": d.description,
        "category": d.category,
        "image": d.image,
        "images": images_list,
        "budget": d.budget,
        "hidden_gem_score": d.hidden_gem_score,
        "best_time_to_visit": d.best_time_to_visit,
        "latitude": d.latitude,
        "longitude": d.longitude,
        "famous_dish": d.famous_dish,
        "famous_tradition": d.famous_tradition,
        "famous_places": d.famous_places,
        "festivals": d.festivals,
        "fun_fact": d.fun_fact
    }


@destination_bp.route("/destinations", methods=["GET"])
def get_destinations():
    destinations = Destination.query.all()
    return jsonify([destination_to_dict(d) for d in destinations]), 200


@destination_bp.route("/destinations/<int:destination_id>", methods=["GET"])
def get_destination(destination_id):
    d = Destination.query.get(destination_id)
    if not d:
        return jsonify({"error": "Destination not found"}), 404
    return jsonify(destination_to_dict(d)), 200


@destination_bp.route("/destinations", methods=["POST"])
def create_destination():
    data = request.get_json()

    name = data.get("name")
    province = data.get("province")
    description = data.get("description")

    if not name or not province or not description:
        return jsonify({"error": "name, province and description are required"}), 400

    images_list = data.get("images")
    images_json = json.dumps(images_list) if images_list else None

    new_destination = Destination(
        name=name,
        province=province,
        city=data.get("city"),
        description=description,
        category=data.get("category"),
        image=data.get("image"),
        images=images_json,
        budget=data.get("budget"),
        hidden_gem_score=data.get("hidden_gem_score"),
        best_time_to_visit=data.get("best_time_to_visit"),
        latitude=data.get("latitude"),
        longitude=data.get("longitude"),
        famous_dish=data.get("famous_dish"),
        famous_tradition=data.get("famous_tradition"),
        famous_places=data.get("famous_places"),
        festivals=data.get("festivals"),
        fun_fact=data.get("fun_fact")
    )

    db.session.add(new_destination)
    db.session.commit()

    return jsonify({"message": "Destination created", "id": new_destination.id}), 201


@destination_bp.route("/destinations/<int:destination_id>", methods=["PUT"])
def update_destination(destination_id):
    d = Destination.query.get(destination_id)
    if not d:
        return jsonify({"error": "Destination not found"}), 404

    data = request.get_json()

    d.name = data.get("name", d.name)
    d.province = data.get("province", d.province)
    d.city = data.get("city", d.city)
    d.description = data.get("description", d.description)
    d.category = data.get("category", d.category)
    d.image = data.get("image", d.image)

    if "images" in data:
        d.images = json.dumps(data.get("images")) if data.get("images") else None

    d.budget = data.get("budget", d.budget)
    d.hidden_gem_score = data.get("hidden_gem_score", d.hidden_gem_score)
    d.best_time_to_visit = data.get("best_time_to_visit", d.best_time_to_visit)
    d.latitude = data.get("latitude", d.latitude)
    d.longitude = data.get("longitude", d.longitude)
    d.famous_dish = data.get("famous_dish", d.famous_dish)
    d.famous_tradition = data.get("famous_tradition", d.famous_tradition)
    d.famous_places = data.get("famous_places", d.famous_places)
    d.festivals = data.get("festivals", d.festivals)
    d.fun_fact = data.get("fun_fact", d.fun_fact)

    db.session.commit()

    return jsonify({"message": "Destination updated"}), 200


@destination_bp.route("/destinations/<int:destination_id>", methods=["DELETE"])
def delete_destination(destination_id):
    d = Destination.query.get(destination_id)
    if not d:
        return jsonify({"error": "Destination not found"}), 404

    db.session.delete(d)
    db.session.commit()

    return jsonify({"message": "Destination deleted"}), 200