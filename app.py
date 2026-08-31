import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from config import Config
from database import db

load_dotenv()


from models.user import User
from models.destination import Destination
from models.trip import Trip
from models.review import Review
from models.user_location import UserLocation
from models.package import Package
from models.hotel import Hotel
from models.transport import Transport
from models.booking import Booking
 

from routes.auth_routes import auth_bp
from routes.destination_routes import destination_bp
from routes.trip_routes import trip_bp
from routes.review_routes import review_bp
from routes.location_routes import location_bp
from routes.ai_routes import ai_bp
from routes.translate_routes import translate_bp
from routes.package_routes import package_bp


app = Flask(__name__)
app.config.from_object(Config)

CORS(app, origins="*")
 # Initialize Database
db.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(destination_bp)
app.register_blueprint(trip_bp)
app.register_blueprint(review_bp)
app.register_blueprint(location_bp)
app.register_blueprint(ai_bp)
app.register_blueprint(translate_bp)
app.register_blueprint(package_bp)
from routes.hotel_routes import hotel_bp

from routes.transport_routes import transport_bp
app.register_blueprint(transport_bp)

from routes.budget_routes import budget_bp
app.register_blueprint(budget_bp)

from routes.booking_routes import booking_bp
app.register_blueprint(booking_bp)

from routes.itinerary_routes import itinerary_bp
app.register_blueprint(itinerary_bp)

from routes.vedhi_routes import vedhi_bp
app.register_blueprint(vedhi_bp)

from routes.pin_routes import pin_bp
app.register_blueprint(pin_bp)

app.register_blueprint(hotel_bp)

 @app.route("/")
def home():
    return "PakExplorer AI Backend is Running!"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
