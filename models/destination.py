from database import db

class Destination(db.Model):
    __tablename__ = "destinations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    province = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100))
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50))
    image = db.Column(db.String(255))
    images = db.Column(db.Text)
    budget = db.Column(db.Float)
    hidden_gem_score = db.Column(db.Float)
    best_time_to_visit = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    famous_dish = db.Column(db.String(255))
    famous_tradition = db.Column(db.String(255))
    famous_places = db.Column(db.Text)
    festivals = db.Column(db.Text)
    fun_fact = db.Column(db.Text)
    required_documents = db.Column(db.Text)  # comma-separated, e.g. "CNIC, Nikah Nama (for couples), Passport-size photo"
    included_activities = db.Column(db.Text)  # comma-separated, e.g. "Guided city tour, Breakfast, Airport pickup"
    excluded_activities = db.Column(db.Text)  # comma-separated, e.g. "Personal shopping, Adventure sports insurance"
    policy_notes = db.Column(db.Text)  # destination-specific terms & conditions, free text

    def __repr__(self):
        return f"<Destination {self.name}>"