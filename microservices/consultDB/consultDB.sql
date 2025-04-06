from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# --- Configuration for PostgreSQL ---
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI', 'postgresql://postgres:postgres@localhost:5432/teledoc')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Models ---
class Schedule(db.Model):
    __tablename__ = 'schedule'
    doctorname = db.Column(db.String(100), primary_key=True)
    next_available_time = db.Column(db.DateTime)
    roomID= db.Column(db.varchar(20))

class ConsultationBooking(db.Model):
    __tablename__ = 'consultation_booking'

    patientFirstName = db.Column(db.String(100), primary_key=True)
    datetime = db.Column(db.DateTime, primary_key=True)

    doctorName = db.Column(db.String(100), db.ForeignKey('schedule.doctorname'), nullable=False)
    roomID = db.Column(db.varchar(20), nullable=False)  # FK to be set based on schedule context logic
    symptom = db.Column(db.String(1000), nullable=False)

    schedule = db.relationship('Schedule', backref='consultations')
