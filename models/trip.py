from database import db

class Trip(db.Model):
    __tablename__ = "trips"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    destination_id = db.Column(db.Integer, db.ForeignKey("destinations.id"), nullable=False)

    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    total_budget = db.Column(db.Float)

    status = db.Column(db.String(50), default="Planned")

    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f"<Trip {self.id}>"