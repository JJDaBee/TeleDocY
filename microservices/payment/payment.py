from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)

# --- Database Config ---
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DB_URI', 'mysql+mysqlconnector://root:root@mysql:3306/paymentdb'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

# --- Models ---
class Payment(db.Model):
    __tablename__ = 'payments'

    paymentID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.String(36), nullable=False)
    medicine_inventory_list = db.Column(db.JSON, nullable=False)
    prescription = db.Column(db.JSON, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    datetime = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "paymentID": self.paymentID,
            "uuid": self.uuid,
            "medicine_inventory_list": self.medicine_inventory_list,
            "datetime": self.datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "prescription": self.prescription,
            "amount": self.amount
        }

# --- Routes ---
@app.route("/payments", methods=["POST"])
def create_payment():
    data = request.get_json()
    uuid = data.get("uuid")
    med_list = data.get("medicine_inventory_list")
    prescription = data.get("prescription")

    if not uuid or not med_list or prescription is None:
        return jsonify({
            "code": 400,
            "message": "Missing 'uuid', 'medicine_inventory_list', or 'prescription'."
        }), 400

    try:
        amount = sum(item["price"] * item["quantity"] for item in med_list)
        new_payment = Payment(
            uuid=uuid,
            medicine_inventory_list=med_list,
            prescription=prescription,
            amount=amount
        )

        db.session.add(new_payment)
        db.session.commit()

        return jsonify({
            "code": 201,
            "message": "Payment created successfully.",
            "data": new_payment.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "code": 500,
            "message": "An error occurred while creating the payment.",
            "error": str(e)
        }), 500

# --- Get All Payments ---
@app.route("/payments", methods=["GET"])
def get_all_payments():
    try:
        payments = Payment.query.all()
        return jsonify({
            "code": 200,
            "data": [payment.to_dict() for payment in payments]
        }), 200
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": "An error occurred while fetching payments.",
            "error": str(e)
        }), 500


# --- Start App ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5009, debug=True)
