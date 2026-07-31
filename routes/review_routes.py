import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from database import db
from models.review import Review
from utils.auth_utils import token_required

review_bp = Blueprint("review", __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
VALID_TARGET_TYPES = {'destination', 'hotel', 'transport', 'trip'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_upload_folder():
    folder = os.path.join(current_app.root_path, 'static', 'review_images')
    os.makedirs(folder, exist_ok=True)
    return folder


# GET reviews for a target — e.g. /api/reviews?target_type=hotel&target_id=3
@review_bp.route("/api/reviews", methods=["GET"])
def get_reviews():
    target_type = request.args.get('target_type')
    target_id = request.args.get('target_id')

    query = Review.query
    if target_type:
        query = query.filter_by(target_type=target_type)
    if target_id:
        query = query.filter_by(target_id=target_id)

    reviews = query.order_by(Review.created_at.desc()).all()
    return jsonify([r.to_dict() for r in reviews]), 200


# GET average rating + count — e.g. /api/reviews/summary?target_type=hotel&target_id=3
@review_bp.route("/api/reviews/summary", methods=["GET"])
def get_review_summary():
    target_type = request.args.get('target_type')
    target_id = request.args.get('target_id')

    if not target_type or not target_id:
        return jsonify({"error": "target_type and target_id are required"}), 400

    reviews = Review.query.filter_by(target_type=target_type, target_id=target_id).all()
    count = len(reviews)
    avg = round(sum(r.rating for r in reviews) / count, 1) if count > 0 else 0

    return jsonify({"average_rating": avg, "review_count": count}), 200


# POST a new review — multipart/form-data (image upload optional)
# Fields: target_type, target_id, rating, comment, image (file, optional)
@review_bp.route("/api/reviews", methods=["POST"])
@token_required
def create_review():
    target_type = request.form.get('target_type')
    target_id = request.form.get('target_id')
    rating = request.form.get('rating')
    comment = request.form.get('comment', '')

    if not target_type or not target_id or not rating:
        return jsonify({"error": "target_type, target_id, and rating are required"}), 400

    if target_type not in VALID_TARGET_TYPES:
        return jsonify({"error": f"target_type must be one of {sorted(VALID_TARGET_TYPES)}"}), 400

    try:
        rating = int(rating)
        if rating < 1 or rating > 5:
            raise ValueError
    except ValueError:
        return jsonify({"error": "rating must be an integer between 1 and 5"}), 400

    image_url = None
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_name = f"{target_type}_{target_id}_{request.user_id}_{int(__import__('time').time())}_{filename}"
            filepath = os.path.join(get_upload_folder(), unique_name)
            file.save(filepath)
            image_url = f"{request.host_url.rstrip('/')}/static/review_images/{unique_name}"

    new_review = Review(
        user_id=request.user_id,
        target_type=target_type,
        target_id=int(target_id),
        rating=rating,
        comment=comment,
        image_url=image_url
    )

    db.session.add(new_review)
    db.session.commit()

    return jsonify(new_review.to_dict()), 201


@review_bp.route("/api/reviews/<int:review_id>", methods=["DELETE"])
@token_required
def delete_review(review_id):
    review = Review.query.get(review_id)
    if not review or review.user_id != request.user_id:
        return jsonify({"error": "Review not found"}), 404

    db.session.delete(review)
    db.session.commit()

    return jsonify({"message": "Review deleted"}), 200