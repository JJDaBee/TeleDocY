from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI','mysql+mysqlconnector://root:root@mysql:3306/consultationHistory')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)


class consultationHistory(db.Model):
    __tablename__ = "consultationHistory"

    uuid=db.Column(db.Integer, primary_key=True)
    nric=db.Column(db.String(9), autoincrement=False)
    dateTime=db.Column(db.DateTime,primary_key=True)
    reasonForVisit=db.Column(db.String(1000), nullable=False)
    doctorName= db.Column(db.String(100), nullable=False)
    diagnosis=db.Column(db.String(1000), nullable=False)
    prescriptions=db.Column(db.String(1000), default=None)


@app.route("/consultationhistory/<int:uuid>")
def find_by_uuid(uuid):
    # quantity = request.args.get("qty", default=1, type=int)
    indiv_history = consultationHistory.query.filter_by(uuid=uuid).all()

    if not indiv_history:
        return jsonify(
            {
                "code": 404,
                "message": "No consultation history found for this uuid."
            }
        ), 404
    
    indiv_historylist = []
    for record in indiv_history:
        indiv_historylist.append({
            "uuid": record.uuid,
            "nric": record.nric,
            "dateTime": record.dateTime.strftime("%Y-%m-%d %H:%M:%S"),
            "reasonForVisit": record.reasonForVisit,
            "doctorName": record.doctorName,
            "diagnosis": record.diagnosis,
            "prescriptions": record.prescriptions
    })
    
    return jsonify(
        {
            "code":200,
            "data": indiv_historylist
        }
    ), 200

@app.route("/consultationhistory", methods=["POST"])
def create_consultationrecord():
    data = request.get_json()
    uuid= data.get("uuid")
    nric = data.get("nric")
    dateTime = data.get("dateTime")
    reasonForVisit = data.get("reasonForVisit")
    doctorName = data.get("doctorName")
    diagnosis = data.get("diagnosis")
    prescriptions = data.get("prescriptions")

    new_consultation = consultationHistory(
        uuid=uuid,
        nric=nric,
        dateTime=dateTime,
        reasonForVisit=reasonForVisit,
        doctorName=doctorName,
        diagnosis=diagnosis,
        prescriptions=prescriptions
    )
    try:
        # Add the new consultation to the session and commit to the database
        db.session.add(new_consultation)
        db.session.commit()

        return jsonify({
            "code": 201,
            "message": "Consultation record created successfully.",
            "data": {
                "uuid": new_consultation.uuid,
                "nric": new_consultation.nric,
                "dateTime": new_consultation.dateTime.strftime("%Y-%m-%d %H:%M:%S"),
                "reasonforVisit": new_consultation.reasonForVisit,
                "doctorName": new_consultation.doctorName,
                "diagnosis": new_consultation.diagnosis,
                "prescriptions": new_consultation.prescriptions
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "code": 500,
            "message": "An error occurred while creating the consultation record.",
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)