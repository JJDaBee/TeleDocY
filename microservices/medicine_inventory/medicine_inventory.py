from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import subprocess

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI','mysql+mysqlconnector://root:root@mysql:3306/medicineInventory')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)
# project_root = os.path.dirname(os.path.abspath(__file__))
# init_path = os.path.join(project_root, "microservices/medicine_inventory", "medicine_inventory.sql")

class medicineInventory(db.Model):
    __tablename__ = "medicineInventory"

    medicationName = db.Column(db.String(255), primary_key=True, nullable=False)  
    price = db.Column(db.DECIMAL(10, 2), nullable=False) 
    quantityLeft = db.Column(db.Integer, nullable=False, default=0)  
    nextRestockDate = db.Column(db.DateTime, default=None) 
    allergies = db.Column(db.String(1000), default="None")


@app.route("/medicine_inventory/<string:medicationName>")
def find_by_medicationName(medicationName):
    # quantity = request.args.get("qty", default=1, type=int)
    available_meds = medicineInventory.query.filter_by(medicationName=medicationName).first()

    if available_meds:
        return jsonify(
        {
            "code": 200,
            "data": {
                "medicationName": available_meds.medicationName,
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

@app.route("/medicine_inventory", methods=["GET"])
def get_all_medicine():
    all_meds = medicineInventory.query.all()

    if all_meds:
        result = []
        for med in all_meds:
            result.append({
                "medicationName": med.medicationName,
                "price": float(med.price),
                "quantityLeft": med.quantityLeft,
                "isAvailable": med.quantityLeft > 0
            })

        return jsonify({
            "code": 200,
            "data": result
        }), 200

    return jsonify({
        "code": 404,
        "message": "No medicines found in inventory."
    }), 404

@app.route("/medicine_inventory/<string:medicationName>/reduce", methods=["POST"])
# add {
#   "quantity": 2 (example)
# }
# into raw JSON body
def reduce_quantity(medicationName):
    data = request.get_json()
    reduce_by = data.get("quantity", 1)  # Default to 1 if not provided

    medicine = medicineInventory.query.filter_by(medicationName=medicationName).first()

    if not medicine:
        return jsonify({
            "code": 404,
            "message": f"Medicine '{medicationName}' not found."
        }), 404

    if medicine.quantityLeft < reduce_by:
        return jsonify({
            "code": 400,
            "message": "Not enough stock to reduce."
        }), 400

    medicine.quantityLeft -= reduce_by
    db.session.commit()
    # result =subprocess.run([
    #         "docker", "exec", "-i", "teledocy-mysql-1",  # use your container name
    #         "mysqldump", "-u", "root", "-proot", "consultationHistory"
    #     ], stdout=open(init_path, "w"))
    # print("mysqldump executed. Return code:", result.returncode)
    return jsonify({
        "code": 200,
        "message": f"{reduce_by} units deducted from '{medicationName}'.",
        "data": {
            "medicationName": medicine.medicationName,
            "quantityLeft": medicine.quantityLeft
        }
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)