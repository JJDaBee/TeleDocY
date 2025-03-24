import threading
import time
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# PostgreSQL Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/schedule'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Doctor Table Model
class Schedule(db.Model):
    __tablename__ = "schedule"

    doctorname = db.Column(db.String(100), primary_key=True)
    availability = db.Column(db.Boolean, nullable=False)

# Function to reset availability after 30 minutes
def reset_availability_after_delay(doctor_name):
    """ Marks doctor as available after 30 minutes """
    time.sleep(1800)  # Wait for 30 minutes (1800 seconds)
    
    with app.app_context():  # Ensure the Flask app context is available
        doctor = Schedule.query.filter_by(doctorname=doctor_name).first()
        if doctor:
            doctor.availability = True  # Mark as available
            db.session.commit()
            print(f"[INFO] {doctor_name} is now available again.")

# API Endpoint to Get First Available Doctor
@app.route("/availableDoctor", methods=['GET'])
def get_first_available_doctor():
    with app.app_context():
        available_doctor = Schedule.query.filter_by(availability=True).first()

        if available_doctor:
            # Mark doctor as unavailable
            available_doctor.availability = False
            db.session.commit()

            # Start a thread to reset availability after 30 minutes
            reset_thread = threading.Thread(target=reset_availability_after_delay, args=(available_doctor.doctorname,))
            reset_thread.start()

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
    app.run(port=5000, debug=True)

