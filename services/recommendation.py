import math
from models.destination import Destination
from models.user_location import UserLocation


def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def get_recommendations(user_id, category=None, max_budget=None, limit=10):
    query = Destination.query

    if category:
        query = query.filter(Destination.category == category)

    if max_budget:
        query = query.filter(Destination.budget <= max_budget)

    destinations = query.all()

    user_location = UserLocation.query.filter_by(user_id=user_id).first()

    scored = []
    for d in destinations:
        score = 0.0

        # Hidden gem score contributes directly (0-10 scale assumed)
        if d.hidden_gem_score:
            score += d.hidden_gem_score * 2

        # Budget fit: closer to max_budget without exceeding gets a small bonus
        if max_budget and d.budget:
            budget_ratio = d.budget / max_budget
            score += (1 - abs(0.7 - budget_ratio)) * 5

        # Proximity bonus: closer destinations score higher
        distance_km = None
        if user_location and d.latitude and d.longitude:
            distance_km = haversine_distance(
                user_location.latitude, user_location.longitude,
                d.latitude, d.longitude
            )
            proximity_score = max(0, 10 - (distance_km / 50))
            score += proximity_score

        scored.append({
            "id": d.id,
            "name": d.name,
            "province": d.province,
            "city": d.city,
            "category": d.category,
            "budget": d.budget,
            "hidden_gem_score": d.hidden_gem_score,
            "distance_km": round(distance_km, 2) if distance_km is not None else None,
            "score": round(score, 2)
        })

    scored.sort(key=lambda x: x["score"], reverse=True)

    return scored[:limit]