from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from flask_cors import CORS


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DB_URI", "postgresql+psycopg2://postgres:postgres@postgres_consult:5432/consult"
)
CORS(app)  # 🔥 This fixes the CORS error


app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Ensure column names match your SQL file
class Consult(db.Model):
    __tablename__ = 'consults'
    firstname = db.Column(db.String(100), primary_key=True)
    datetime = db.Column(db.DateTime, primary_key=True)
    doctorname = db.Column(db.String(100), nullable=False)
    roomid = db.Column(db.String(20), nullable=False)
    symptom = db.Column(db.Text, nullable=False)
    medicalhistory = db.Column(db.Text, nullable=True)  # Matches SQL column
    uuid = db.Column(db.String(36), nullable=False, unique=True)

    def to_dict(self):
        return {
            'uuid': self.uuid,
            "firstname": self.firstname,
            "datetime": self.datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "doctorname": self.doctorname,
            "roomid": self.roomid,
            "symptom": self.symptom,
            "medicalhistory": self.medicalhistory
        }

@app.route("/consults", methods=["GET"])
def get_all_consults():
    records = Consult.query.all()
    return jsonify({
        "code": 200,
        "data": [record.to_dict() for record in records]
    }), 200

@app.route("/consults", methods=["POST"])
def create_consult():
    data = request.get_json()
    try:
        record = Consult(
            uuid=data["uuid"],
            firstname=data["firstname"],
            datetime=datetime.strptime(data["datetime"], "%Y-%m-%d %H:%M:%S"),
            doctorname=data["doctorname"],
            roomid=data["roomid"],
            symptom=data["symptom"],
            medicalhistory=data.get("medicalhistory")  # Must match class attribute
        )
        db.session.add(record)
        db.session.commit()
        return jsonify({
            "code": 201,
            "message": "Consultation booking created.",
            "data": record.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"code": 500, "message": "Error inserting consult", "error": str(e)}), 500
    
@app.route("/consults/doctor/<string:doctorname>", methods=["GET"])
def get_consults_by_doctor(doctorname):
    try:
        records = Consult.query.filter_by(doctorname=doctorname).all()
        if not records:
            return jsonify({
                "code": 404,
                "message": f"No consults found for doctor: {doctorname}"
            }), 404

        return jsonify({
            "code": 200,
            "data": [record.to_dict() for record in records]
        }), 200
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": "Error fetching consults by doctor.",
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5008, debug=True)
