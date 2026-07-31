from database import db


class DestinationPin(db.Model):
    __tablename__ = "destination_pins"

    id = db.Column(db.Integer, primary_key=True)
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(50))  # e.g. "Bazaar", "Famous Place", "Viewpoint", "Food Street"
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))  # main thumbnail
    images = db.Column(db.Text)  # comma-separated gallery image URLs

    def to_dict(self):
        return {
            "id": self.id,
            "destination_id": self.destination_id,
            "name": self.name,
            "category": self.category,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "description": self.description,
            "image_url": self.image_url,
            "images": [i.strip() for i in self.images.split(",") if i.strip()] if self.images else []
        }