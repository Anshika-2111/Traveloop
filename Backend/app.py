from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from extensions import db
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
db.init_app(app)
bcrypt = Bcrypt(app)

from models import User, Trip, Stop, Activity

# Create tables on Render / SQLite automatically
with app.app_context():
    db.create_all()
    print("Tables created successfully!")


@app.route("/")
def home():
    return "Traveloop Backend Running Successfully!"


@app.route("/signup", methods=["POST"])
def signup():
    data = request.json

    existing_user = User.query.filter_by(email=data.get("email")).first()

    if existing_user:
        return jsonify({
            "message": "Email already exists. Redirecting to login...",
            "redirect": "login"
        }), 400

    hashed_password = bcrypt.generate_password_hash(
        data.get("password")
    ).decode("utf-8")

    new_user = User(
        name=data.get("name"),
        email=data.get("email"),
        password=hashed_password
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "Account created successfully",
        "user": {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email
        }
    }), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.json

    user = User.query.filter_by(email=data.get("email")).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    if not bcrypt.check_password_hash(user.password, data.get("password")):
        return jsonify({"message": "Invalid password"}), 401

    return jsonify({
        "message": "Login successful",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }), 200


@app.route("/trips", methods=["POST"])
def create_trip():
    data = request.json

    new_trip = Trip(
        user_id=data.get("user_id"),
        title=data.get("title"),
        description=data.get("description"),
        start_date=data.get("start_date"),
        end_date=data.get("end_date"),
        budget=data.get("budget")
    )

    db.session.add(new_trip)
    db.session.commit()

    return jsonify({"message": "Trip created successfully"}), 201


@app.route("/trips/<int:user_id>", methods=["GET"])
def get_trips(user_id):
    trips = Trip.query.filter_by(user_id=user_id).all()

    trip_list = []

    for trip in trips:
        trip_list.append({
            "id": trip.id,
            "title": trip.title,
            "description": trip.description,
            "start_date": trip.start_date,
            "end_date": trip.end_date,
            "budget": trip.budget
        })

    return jsonify(trip_list), 200


@app.route("/trips/<int:trip_id>/stops", methods=["POST"])
def add_stop(trip_id):
    data = request.json

    new_stop = Stop(
        trip_id=trip_id,
        city_name=data.get("city_name"),
        country=data.get("country"),
        start_date=data.get("start_date"),
        end_date=data.get("end_date"),
        order_no=data.get("order_no", 1)
    )

    db.session.add(new_stop)
    db.session.commit()

    return jsonify({"message": "Stop added successfully"}), 201


@app.route("/trips/<int:trip_id>/stops", methods=["GET"])
def get_stops(trip_id):
    stops = Stop.query.filter_by(trip_id=trip_id).all()

    stops_list = []

    for stop in stops:
        stops_list.append({
            "id": stop.id,
            "city_name": stop.city_name,
            "country": stop.country,
            "start_date": stop.start_date,
            "end_date": stop.end_date,
            "order_no": stop.order_no
        })

    return jsonify(stops_list), 200


@app.route("/stops/<int:stop_id>", methods=["DELETE"])
def delete_stop(stop_id):
    stop = Stop.query.get(stop_id)

    if not stop:
        return jsonify({"message": "Stop not found"}), 404

    activities = Activity.query.filter_by(stop_id=stop_id).all()

    for activity in activities:
        db.session.delete(activity)

    db.session.delete(stop)
    db.session.commit()

    return jsonify({"message": "Stop deleted successfully"}), 200


@app.route("/stops/<int:stop_id>/activities", methods=["POST"])
def add_activity(stop_id):
    data = request.json

    new_activity = Activity(
        stop_id=stop_id,
        name=data.get("name"),
        activity_type=data.get("activity_type"),
        cost=data.get("cost"),
        duration=data.get("duration"),
        activity_date=data.get("activity_date"),
        notes=data.get("notes")
    )

    db.session.add(new_activity)
    db.session.commit()

    return jsonify({"message": "Activity added successfully"}), 201


@app.route("/stops/<int:stop_id>/activities", methods=["GET"])
def get_activities(stop_id):
    activities = Activity.query.filter_by(stop_id=stop_id).all()

    activities_list = []

    for activity in activities:
        activities_list.append({
            "id": activity.id,
            "name": activity.name,
            "activity_type": activity.activity_type,
            "cost": activity.cost,
            "duration": activity.duration,
            "activity_date": activity.activity_date,
            "notes": activity.notes
        })

    return jsonify(activities_list), 200


@app.route("/activities/<int:activity_id>", methods=["DELETE"])
def delete_activity(activity_id):
    activity = Activity.query.get(activity_id)

    if not activity:
        return jsonify({"message": "Activity not found"}), 404

    db.session.delete(activity)
    db.session.commit()

    return jsonify({"message": "Activity deleted successfully"}), 200


@app.route("/trips/<int:trip_id>", methods=["DELETE"])
def delete_trip(trip_id):
    trip = Trip.query.get(trip_id)

    if not trip:
        return jsonify({"message": "Trip not found"}), 404

    stops = Stop.query.filter_by(trip_id=trip_id).all()

    for stop in stops:
        activities = Activity.query.filter_by(stop_id=stop.id).all()

        for activity in activities:
            db.session.delete(activity)

        db.session.delete(stop)

    db.session.delete(trip)
    db.session.commit()

    return jsonify({"message": "Trip deleted successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True)