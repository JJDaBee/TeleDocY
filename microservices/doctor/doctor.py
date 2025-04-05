import os
import subprocess
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# PostgreSQL Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI', 'postgresql+psycopg2://postgres:postgres@localhost:5432/doctor')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

class Doctor(db.Model):
    __tablename__ = "doctor"

    doctorid = db.Column(db.String)
    gender = db.Column(db.String(20))
    dateofbirth = db.Column(db.Date)
    email = db.Column(db.String(150))
    phone = db.Column(db.String(20))
    yearsofexperience = db.Column(db.Integer)
    medicallicensenumber = db.Column(db.String(100))
    doctorname = db.Column(db.String(200), nullable=False, primary_key=True)
    picture = db.Column(db.String)

@app.route("/doctor/<string:doctorName>")
def get_doctor_info(doctorName):
    doctor = Doctor.query.filter_by(doctorname=doctorName).first()

    if doctor:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "gender": doctor.gender,
                    "picture": doctor.picture
                }
            }
        ), 200

    return jsonify(
        {
            "code": 404,
            "message": "Doctor not found."
        }
    ), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5007, debug=True)