from database import db

class Package(db.Model):
    __tablename__ = "packages"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    duration_days = db.Column(db.Integer, nullable=False)
    price_per_person = db.Column(db.Float, nullable=False)
    group_size = db.Column(db.String(50))
    image = db.Column(db.String(255))
    images = db.Column(db.Text)
    short_description = db.Column(db.Text, nullable=False)
    inclusions = db.Column(db.Text)
    itinerary_summary = db.Column(db.Text)
    rating = db.Column(db.Float)

    # --- new fields ---
    itinerary_days = db.Column(db.Text)          # JSON: [{"day":1,"title":"...","description":"..."}]
    available_days = db.Column(db.String(100))   # e.g. "Everyday" or "Fri - Sun"
    contact_number = db.Column(db.String(30))
    vibe_tagline = db.Column(db.String(150))     # e.g. "A Romantic Escape for Two"

    def __repr__(self):
        return f"<Package {self.title}>"