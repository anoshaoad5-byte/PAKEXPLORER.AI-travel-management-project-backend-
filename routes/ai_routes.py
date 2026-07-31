from flask import Blueprint, request, jsonify
from utils.auth_utils import token_required
from services.recommendation import get_recommendations
ai_bp = Blueprint("ai", __name__)


@ai_bp.route("/recommendations", methods=["GET"])
@token_required
def recommendations():
    category = request.args.get("category")
    max_budget = request.args.get("max_budget", type=float)
    limit = request.args.get("limit", default=10, type=int)

    results = get_recommendations(
        user_id=request.user_id,
        category=category,
        max_budget=max_budget,
        limit=limit
    )

    return jsonify(results), 200