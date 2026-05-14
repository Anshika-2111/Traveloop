from extensions import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.String(50))
    end_date = db.Column(db.String(50))
    budget = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Stop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey("trip.id"), nullable=False)
    city_name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100))
    start_date = db.Column(db.String(50))
    end_date = db.Column(db.String(50))
    order_no = db.Column(db.Integer, default=1)

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stop_id = db.Column(db.Integer, db.ForeignKey("stop.id"), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    activity_type = db.Column(db.String(100))
    cost = db.Column(db.Float, default=0)
    duration = db.Column(db.String(50))
    activity_date = db.Column(db.String(50))
    notes = db.Column(db.Text)