from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/medicineInventory'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}


db = SQLAlchemy(app)

class medicineInventory(db.Model):
    __tablename__ = "medicineInventory"

    medicationID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    medication = db.Column(db.String(255), nullable=False)  
    price = db.Column(db.DECIMAL(10, 2), nullable=False) 
    quantityLeft = db.Column(db.Integer, nullable=False, default=0)  
    nextRestockDate = db.Column(db.DateTime, default=None) 
    allergies = db.Column(db.String(1000), default="None")


@app.route("/medicineInventory/<string:medicationID>")
def find_by_medicationID(medicationID):
    # quantity = request.args.get("qty", default=1, type=int)
    available_meds = medicineInventory.query.filter_by(medicationID=medicationID).first()


    if available_meds:
        return jsonify(
        {
            "code": 200,
            "data": {
                "medicationID": available_meds.medicationID,
                "medication": available_meds.medication,
                "price": float(available_meds.price),
                "quantityLeft": available_meds.quantityLeft,
                "isAvailable": available_meds.quantityLeft > 0,
                # "sufficientStock": (available_meds.quantityLeft >= quantity) if quantity is not None else None
            }
        }
    ), 200
    return jsonify(
        {
            "code": 404,
            "message": "medicine not available."
        }
    ), 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)