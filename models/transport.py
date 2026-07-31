from database import db
from datetime import datetime


class Transport(db.Model):
    __tablename__ = 'transports'

    id = db.Column(db.Integer, primary_key=True)
    provider_name = db.Column(db.String(150), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    from_city = db.Column(db.String(100), nullable=False)
    to_city = db.Column(db.String(100), nullable=False)
    departure_time = db.Column(db.String(20), nullable=True)
    arrival_time = db.Column(db.String(20), nullable=True)
    price = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Float, default=0.0)
    image_url = db.Column(db.String(300), nullable=True)
    amenities = db.Column(db.String(500), nullable=True)
    seats_available = db.Column(db.Integer, default=0)
    contact_number = db.Column(db.String(30), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "provider_name": self.provider_name,
            "type": self.type,
            "from_city": self.from_city,
            "to_city": self.to_city,
            "departure_time": self.departure_time,
            "arrival_time": self.arrival_time,
            "price": self.price,
            "rating": self.rating,
            "image_url": self.image_url,
            "amenities": self.amenities.split(",") if self.amenities else [],
            "seats_available": self.seats_available,
            "contact_number": self.contact_number,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }