import os
import subprocess
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# PostgreSQL Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI', 'postgresql+psycopg2://postgres:postgres@localhost:5432/doctor')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Doctor(db.Model):
    __tablename__ = "doctor"

    doctorID = db.Column(db.String, primary_key=True)
    doctorName = db.Column(db.String(200), nullable=False)
    gender = db.Column(db.String(20))
    dateOfBirth = db.Column(db.Date)
    email = db.Column(db.String(150))
    phone = db.Column(db.String(20))
    credentials = db.Column(db.String(50))
    yearsOfExperience = db.Column(db.Integer)
    medicalLicenseNumber = db.Column(db.String(100))

if __name__ == '__main__':
    app.run(port=5500, debug=True)