from datetime import datetime, timedelta
import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# PostgreSQL Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI', 'postgresql+psycopg2://postgres:postgres@postgres_schedule:5432/schedule')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Doctor Table Model
class Schedule(db.Model):
    __tablename__ = "schedule"

    doctorname = db.Column(db.String(100), primary_key=True)
    next_available_time = db.Column(db.DateTime, nullable=True)
    roomid = db.Column(db.String(20), nullable=False)

# API Endpoint to Get First Available Doctor
@app.route("/schedule", methods=['GET'])
def get_first_available_doctor():
    now = datetime.utcnow()

    # Step 1: Reset expired doctors (whose slots have passed)
    expired_doctors = Schedule.query.filter(
        Schedule.next_available_time <= now
    ).all()

    for doctor in expired_doctors:
        doctor.next_available_time = None

    if expired_doctors:
        db.session.commit()

    # Step 2: Find the first currently available doctor
    available_doctor = Schedule.query.filter(
        Schedule.next_available_time == None
    ).first()

    if available_doctor:
        # Step 3: Block the doctor for 30 minutes
        available_doctor.next_available_time = now + timedelta(seconds=60)
        db.session.commit()

        return jsonify({
            "code": 200,
            "data": {
                "doctorName": available_doctor.doctorname,
                "roomid": available_doctor.roomid
            }
        }), 200

    # Step 4: No doctors available
    return jsonify({
        "code": 404,
        "message": "No available doctors at the moment."
    }), 404

@app.route("/schedule/all", methods=["GET"])
def get_all_doctors():
    now = datetime.utcnow()

    # Step 1: Reset any expired doctors
    expired_doctors = Schedule.query.filter(
        Schedule.next_available_time <= now
    ).all()

    for doctor in expired_doctors:
        doctor.next_available_time = None

    if expired_doctors:
        db.session.commit()

    # Step 2: Return all doctors with updated availability
    doctors = Schedule.query.all()

    if not doctors:
        return jsonify({
            "code": 404,
            "message": "No doctors found in schedule."
        }), 404

    doctor_list = []
    for doc in doctors:
        doctor_list.append({
            "doctorName": doc.doctorname,
            "roomid": doc.roomid,
            "nextAvailableTime": doc.next_available_time.strftime("%Y-%m-%d %H:%M:%S") if doc.next_available_time else None
        })

    return jsonify({
        "code": 200,
        "data": doctor_list
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006, debug=True)