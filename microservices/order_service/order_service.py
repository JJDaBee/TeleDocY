from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import subprocess
app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI','mysql+mysqlconnector://root:root@mysql:3306/orderService')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}
db = SQLAlchemy(app)
project_root = os.path.dirname(os.path.abspath(__file__))
init_path = os.path.join(project_root, "microservices/order_services", "order_services.sql")
# Medicine Inventory Model
#class medicineInventory(db.Model):
#    __tablename__ = "medicineInventory"  # Matches MySQL table name exactly

#    medication = db.Column(db.String(255), primary_key=True)  # Medication as Primary Key
#    price = db.Column(db.DECIMAL(10, 2), nullable=False) 
#    quantityLeft = db.Column(db.Integer, nullable=False, default=0)  
#    nextRestockDate = db.Column(db.DateTime, default=None) 
#    allergies = db.Column(db.String(1000), default="None")

# Orders Model
class Order(db.Model):
    __tablename__ = "orderService"

    orderID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid=db.Column(db.String(20), primary_key=True)
    nric = db.Column(db.String(9), nullable=False)  # User Identifier
#    medication = db.Column(db.String(255), db.ForeignKey('medicineInventory.medication'), nullable=False)  # Matches MySQL table name
    medication = db.Column(db.String(255), nullable=False)
    dosage = db.Column(db.String(255), nullable=False)
    numberOfPills = db.Column(db.Integer, nullable=False)
    prescriptionDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    #creditCard = db.Column(db.String(100), nullable=False)  # Needs Encryption in Production

    #medicine = db.relationship("medicineInventory", backref="orders")

# Initialize the Database
#with app.app_context():
#    db.create_all()

# API Route to Place an Order
@app.route("/order/", methods=["POST"])
def place_order():
    data = request.json

    # Extract Data from Request
    orderID = data.get("orderID")
    uuid = data.get("uuid")
    nric = data.get("nric")
    medication = data.get("medication")
    dosage = data.get("dosage")
    numberOfPills = data.get("numberOfPills")
    prescriptionDate = data.get("prescriptionDate")
    #creditCard = data.get("creditCard")

    new_order = Order(
            orderID = orderID,
            uuid=uuid,
            nric=nric,
            medication=medication,
            dosage=dosage,
            numberOfPills=numberOfPills,
            prescriptionDate=datetime.strptime(prescriptionDate, "%Y-%m-%d %H:%M:%S"),
    #        creditCard=creditCard
        )

    # Validate Required Fields
    #if not all([orderID,uuid,nric, medication, dosage, numberOfPills, prescriptionDate, creditCard]):
    #    return jsonify({"code": 400, "message": "Missing required fields"}), 400

    # Check if Medication Exists in Inventory
    #medicine =medicineInventory.query.filter_by(medication=medication_name).first()

    #if not medicine:
    #    return jsonify({
    #        "code": 404,
    #        "message": f"Medication '{medication_name}' not found in inventory."
    #    }), 404

    # Check Stock Availability
    #if medicine.quantityLeft < numberOfPills:
    #    return jsonify({
    #       "code": 400,
    #        "message": f"Not enough stock for '{medication_name}'. Available: {medicine.quantityLeft}, Requested: {numberOfPills}."
    #    }), 400

    # Deduct Stock
    #medicine.quantityLeft -= numberOfPills
    #db.session.commit()  # Save stock update

    # Create New Order
    try:
        db.session.add(new_order)
        db.session.commit()
        result =subprocess.run([
                    "docker", "exec", "-i", "teledocy-mysql-1",  # use your container name
                    "mysqldump", "-u", "root", "-proot", "consultationHistory"
                ], stdout=open(init_path, "w"))
        print("mysqldump executed. Return code:", result.returncode)
        return jsonify({
            "code": 201,
            "message": "Order placed successfully!",
            "data": {
                "orderID": new_order.orderID,
                "uuid": new_order.uuid,
                "nric": new_order.nric,
                "medication": new_order.medication,
                "dosage": new_order.dosage,
                "numberOfPills": new_order.numberOfPills,
                "prescriptionDate": new_order.prescriptionDate
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"code": 500, "message": f"Internal Server Error: {str(e)}"}), 500

# Run Flask App
if __name__ == '__main__':
    app.run(port=5600, debug=True
    )