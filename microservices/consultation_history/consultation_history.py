from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
import os
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI', 'mysql+mysqlconnector://root:root@mysql:3306/consultationHistory')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

class consultationHistory(db.Model):
    __tablename__ = "consultationHistory"

    uuid = db.Column(db.String(20), primary_key=True)
    dateTime = db.Column(db.DateTime, primary_key=True)
    reasonForVisit = db.Column(db.String(1000), nullable=False)
    doctorName = db.Column(db.String(100), nullable=False)
    diagnosis = db.Column(db.String(1000), nullable=False)
    prescriptions = db.Column(db.JSON, default=None)

@app.route("/consultation_history", methods=["GET"])
def get_all_consultation_records():
    try:
        all_records = consultationHistory.query.all()
        if not all_records:
            return jsonify({"code": 404, "message": "No consultation history records found."}), 404

        records_list = []
        for record in all_records:
            records_list.append({
                "uuid": record.uuid,
                "dateTime": record.dateTime.strftime("%Y-%m-%d %H:%M:%S"),
                "reasonForVisit": record.reasonForVisit,
                "doctorName": record.doctorName,
                "diagnosis": record.diagnosis,
                "prescriptions": record.prescriptions
            })

        return jsonify({"code": 200, "data": records_list}), 200

    except Exception as e:
        return jsonify({"code": 500, "message": "Error fetching records.", "error": str(e)}), 500

@app.route("/consultation_history/<string:uuid>")
def find_by_uuid(uuid):
    records = consultationHistory.query.filter_by(uuid=uuid).all()

    if not records:
        return jsonify({"code": 404, "message": "No consultation history found for this uuid."}), 404

    history_list = []
    for record in records:
        history_list.append({
            "uuid": record.uuid,
            "dateTime": record.dateTime.strftime("%Y-%m-%d %H:%M:%S"),
            "reasonForVisit": record.reasonForVisit,
            "doctorName": record.doctorName,
            "diagnosis": record.diagnosis,
            "prescriptions": record.prescriptions
        })

    return jsonify({"code": 200, "data": history_list}), 200

@app.route("/consultation_history", methods=["POST"])
def create_consultation_record():
    data = request.get_json()
    uuid = data.get("uuid")
    dateTime_str = data.get("dateTime")
    reasonForVisit = data.get("reasonForVisit")
    doctorName = data.get("doctorName")
    diagnosis = data.get("diagnosis")
    prescriptions = data.get("prescriptions")

    try:
        dateTime = datetime.strptime(dateTime_str, "%Y-%m-%d %H:%M:%S")
    except Exception as e:
        return jsonify({
            "code": 400,
            "message": "Invalid dateTime format. Expected 'YYYY-MM-DD HH:MM:SS'.",
            "error": str(e)
        }), 400

    new_record = consultationHistory(
        uuid=uuid,
        dateTime=dateTime,
        reasonForVisit=reasonForVisit,
        doctorName=doctorName,
        diagnosis=diagnosis,
        prescriptions=prescriptions
    )

    try:
        db.session.add(new_record)
        db.session.commit()
        return jsonify({
            "code": 201,
            "message": "Consultation record created successfully.",
            "data": {
                "uuid": new_record.uuid,
                "dateTime": new_record.dateTime.strftime("%Y-%m-%d %H:%M:%S"),
                "reasonForVisit": new_record.reasonForVisit,
                "doctorName": new_record.doctorName,
                "diagnosis": new_record.diagnosis,
                "prescriptions": new_record.prescriptions
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "code": 500,
            "message": "Error creating consultation record.",
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
