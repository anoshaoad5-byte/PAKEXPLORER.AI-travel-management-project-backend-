from database import db
from datetime import datetime


class Hotel(db.Model):
    __tablename__ = 'hotels'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    price_per_night = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Float, default=0.0)
    image_url = db.Column(db.String(300), nullable=True)
    amenities = db.Column(db.String(500), nullable=True)
    rooms_available = db.Column(db.Integer, default=0)
    contact_number = db.Column(db.String(30), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "address": self.address,
            "description": self.description,
            "price_per_night": self.price_per_night,
            "rating": self.rating,
            "image_url": self.image_url,
            "amenities": self.amenities.split(",") if self.amenities else [],
            "rooms_available": self.rooms_available,
            "contact_number": self.contact_number,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }