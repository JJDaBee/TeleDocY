from datetime import datetime, timedelta
import os
import subprocess
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# PostgreSQL Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI', 'postgresql+psycopg2://postgres:postgres@localhost:5432/schedule')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Doctor Table Model
class Schedule(db.Model):
    __tablename__ = "schedule"

    doctorname = db.Column(db.String(100), primary_key=True)
    next_available_time = db.Column(db.DateTime, nullable=True)

# API Endpoint to Get First Available Doctor
@app.route("/schedule", methods=['GET'])
def get_first_available_doctor():
    now = datetime.utcnow()

    # Find a doctor who is available right now (or never assigned before)
    available_doctor = Schedule.query.filter(
        (Schedule.next_available_time == None) | (Schedule.next_available_time <= now)
    ).first()

    if available_doctor:
        # Set the doctor to be unavailable for the next 30 minutes
        available_doctor.next_available_time = datetime.utcnow() + timedelta(minutes=30) # RMB TO CHANGE BACK TO 30 MINUTES!!

        db.session.commit()

        return jsonify({
            "code": 200,
            "data": {
                "doctorName": available_doctor.doctorname
            }
        }), 200

    return jsonify({
        "code": 404,
        "message": "No available doctors at the moment."
    }), 404

if __name__ == '__main__':
    app.run(port=5400, debug=True)