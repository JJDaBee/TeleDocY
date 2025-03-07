from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/consultationHistory'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

class consultationHistory(db.Model):
    __tablename__ = "consultationHistory"

    NRIC=db.Column(db.String(9), primary_key=True, autoincrement=False)
    dateTime=db.Column(db.DateTime,primary_key=True)
    reasonforVisit=db.Column(db.String(1000), nullable=False)
    doctorName= db.Column(db.String(100), nullable=False)
    diagnosis=db.Column(db.String(1000), nullable=False)
    prescriptions=db.Column(db.String(1000), default=None)


@app.route("/consultationHistory/<string:NRIC>")
def find_by_NRIC(NRIC):
    # quantity = request.args.get("qty", default=1, type=int)
    indiv_history = consultationHistory.query.filter_by(NRIC=NRIC).all()

    if not indiv_history:
        return jsonify(
            {
                "code": 404,
                "message": "No consultation history found for this NRIC."
            }
        ), 404
    
    indiv_historylist = []
    for record in indiv_history:
        indiv_historylist.append({
            "dateTime": record.dateTime.strftime("%Y-%m-%d %H:%M:%S"),
            "reasonforVisit": record.reasonforVisit,
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


if __name__ == '__main__':
    app.run(port=5000, debug=True)