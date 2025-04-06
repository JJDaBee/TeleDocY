from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI', 'mysql+mysqlconnector://root:root@mysql:3306/payment')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

class Payment(db.Model):
    __tablename__ = "payment"

    paymentID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    datetime = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "paymentID": self.paymentID,
            "amount": float(self.amount),
            "datetime": self.datetime.strftime("%Y-%m-%d %H:%M:%S")
        }

# Create a payment (just for testing purpose, no external logic)
@app.route("/payment", methods=["POST"])
def create_payment():
    data = request.get_json()
    amount = data.get("amount")

    if amount is None:
        return jsonify({"code": 400, "message": "Missing 'amount' in request."}), 400

    new_payment = Payment(amount=amount)
    db.session.add(new_payment)
    db.session.commit()

    return jsonify({
        "code": 201,
        "message": "Payment record created.",
        "data": new_payment.to_dict()
    }), 201

# Get payment by paymentID
@app.route("/payment/<int:paymentID>", methods=["GET"])
def get_payment_by_id(paymentID):
    payment = Payment.query.get(paymentID)
    if not payment:
        return jsonify({"code": 404, "message": "No payment found for this ID."}), 404

    return jsonify({
        "code": 200,
        "data": payment.to_dict()
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5009, debug=True)
