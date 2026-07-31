from database import db
from datetime import datetime


class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(30), nullable=True)

    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'), nullable=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.id'), nullable=True)
    transport_id = db.Column(db.Integer, db.ForeignKey('transports.id'), nullable=True)
    package_id = db.Column(db.Integer, db.ForeignKey('packages.id'), nullable=True)  # new

    members = db.Column(db.Integer, nullable=False, default=1)
    travel_date = db.Column(db.String(30), nullable=True)
    nights = db.Column(db.Integer, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    payment_method = db.Column(db.String(50), nullable=True)  # new: 'jazzcash' / 'easypaisa' / 'cash'
    refund_percentage = db.Column(db.Float, nullable=True)  # new: set on cancellation
    total_amount = db.Column(db.Float, nullable=True)  # new: auto-calculated budget

    status = db.Column(db.String(20), nullable=False, default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "destination_id": self.destination_id,
            "hotel_id": self.hotel_id,
            "transport_id": self.transport_id,
            "package_id": self.package_id,
            "members": self.members,
            "travel_date": self.travel_date,
            "nights": self.nights,
            "notes": self.notes,
            "payment_method": self.payment_method,
            "refund_percentage": self.refund_percentage,
            "total_amount": self.total_amount,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }