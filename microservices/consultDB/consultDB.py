from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from flask_cors import CORS

app = Flask(__name__)

# --- Configuration for PostgreSQL ---
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI', 'postgresql://postgres:postgres@localhost:5432/teledoc')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
db = SQLAlchemy(app)

# --- Models ---
class Schedule(db.Model):
    __tablename__ = 'schedule'
    doctorname = db.Column(db.String(100), primary_key=True)
    next_available_time = db.Column(db.DateTime)
    roomID = db.Column(db.String(20))  # Fixed typo: changed from db.varchar to db.String

class ConsultationBooking(db.Model):
    __tablename__ = 'consultation_booking'

    patientFirstName = db.Column(db.String(100), primary_key=True)
    datetime = db.Column(db.DateTime, primary_key=True)

    doctorName = db.Column(db.String(200), db.ForeignKey('schedule.doctorname'), nullable=False)
    roomID = db.Column(db.String(20), nullable=False)  # Fixed typo: changed from db.varchar to db.String
    symptom = db.Column(db.String(1000), nullable=False)

    # Allows accessing schedule data directly from ConsultationBooking instances
    schedule = db.relationship('Schedule', backref='consultations')

# --- Routes ---
@app.route('/log-symptom', methods=['POST'])
def log_symptom_entry():
    data = request.get_json()

    try:
        consult_time = datetime.strptime(data['datetime'], "%Y-%m-%d %H:%M:%S")

        new_entry = ConsultationBooking(
            patientFirstName=data['patientFirstName'],
            datetime=consult_time,
            doctorName=data['doctorName'],
            roomID=data['roomID'],
            symptom=data['symptom']
        )

        db.session.add(new_entry)
        db.session.commit()

        return jsonify({
            "code": 201,
            "message": "Symptom logged successfully."
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "code": 500,
            "message": f"Failed to log symptom: {str(e)}"
        }), 500

@app.route('/consultation-history', methods=['GET'])
def fetch_all_consultations():
    consultations = ConsultationBooking.query.order_by(ConsultationBooking.datetime.desc()).all()

    return jsonify({
        "code": 200,
        "data": [
            {
                "patientFirstName": c.patientFirstName,
                "datetime": c.datetime.strftime("%Y-%m-%d %H:%M:%S"),
                "doctorName": c.doctorName,
                "roomID": c.roomID,
                "symptom": c.symptom
            }
            for c in consultations
        ]
    }), 200

@app.route('/consultation-history/<string:doctor_name>', methods=['GET'])
def fetch_consultations_by_doctor(doctor_name):
    consultations = ConsultationBooking.query.filter_by(doctorName=doctor_name).order_by(ConsultationBooking.datetime.desc()).all()

    return jsonify({
        "code": 200,
        "data": [
            {
                "patientFirstName": c.patientFirstName,
                "datetime": c.datetime.strftime("%Y-%m-%d %H:%M:%S"),
                "doctorName": c.doctorName,
                "roomID": c.roomID,
                "symptom": c.symptom
            }
            for c in consultations
        ]
    }), 200

# --- Run Server ---
if __name__ == '__main__':
    app.run(port=5500, debug=True)

CORS(app)
