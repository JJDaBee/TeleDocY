from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DB_URI', 'mysql+mysqlconnector://root:root@mysql:3306/deliveryDetail'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

class deliveryDetail(db.Model):
    __tablename__ = "deliveryDetail"

    deliveryID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    deliveryAddress = db.Column(db.String(1000), nullable=False)
    medication = db.Column(db.String(1000), nullable=False)
    deliverySurcharge = db.Column(db.Integer, nullable=False)
    deliveryDate = db.Column(db.DateTime, nullable=False)
    uuid = db.Column(db.String(36), nullable=False)  # UUID string

# ✅ GET all delivery records
@app.route("/delivery_detail", methods=["GET"])
def get_all_delivery_details():
    try:
        deliveries = deliveryDetail.query.all()
        if not deliveries:
            return jsonify({
                "code": 404,
                "message": "No delivery records found."
            }), 404

        result = []
        for d in deliveries:
            result.append({
                "deliveryID": d.deliveryID,
                "deliveryAddress": d.deliveryAddress,
                "medication": d.medication,
                "deliverySurcharge": d.deliverySurcharge,
                "deliveryDate": d.deliveryDate.strftime("%Y-%m-%d %H:%M:%S"),
                "uuid": d.uuid
            })

        return jsonify({
            "code": 200,
            "data": result
        }), 200

    except Exception as e:
        return jsonify({
            "code": 500,
            "message": "An error occurred while fetching delivery details.",
            "error": str(e)
        }), 500

@app.route("/delivery_detail/<int:deliveryID>")
def get_delivery_surcharge(deliveryID):
    delivery_detail = deliveryDetail.query.get(deliveryID)

    if not delivery_detail:
        return jsonify({
            "code": 404,
            "message": "Delivery record not found."
        }), 404

    return jsonify({
        "code": 200,
        "data": {
            "deliverySurcharge": delivery_detail.deliverySurcharge,
        }
    }), 200

# ✅ POST a new delivery record
@app.route("/delivery_detail", methods=["POST"])
def create_delivery_detail():
    try:
        data = request.get_json()

        deliveryAddress = data.get("deliveryAddress")
        medication = data.get("medication")
        deliverySurcharge = data.get("deliverySurcharge")
        deliveryDate = data.get("deliveryDate")  # Optional
        uuid = data.get("uuid")  # Required

        if not (deliveryAddress and medication and deliverySurcharge is not None and uuid):
            return jsonify({
                "code": 400,
                "message": "Missing required fields in request."
            }), 400

        # Default deliveryDate to now + 3 days if not provided
        if deliveryDate:
            deliveryDate = datetime.strptime(deliveryDate, "%Y-%m-%d %H:%M:%S")
        else:
            deliveryDate = datetime.now() + timedelta(days=3)

        new_delivery = deliveryDetail(
            deliveryAddress=deliveryAddress,
            medication=medication,
            deliverySurcharge=deliverySurcharge,
            deliveryDate=deliveryDate,
            uuid=uuid
        )

        db.session.add(new_delivery)
        db.session.commit()

        return jsonify({
            "code": 201,
            "message": "New delivery record created successfully.",
            "data": {
                "deliveryID": new_delivery.deliveryID,
                "deliveryAddress": new_delivery.deliveryAddress,
                "medication": new_delivery.medication,
                "deliverySurcharge": new_delivery.deliverySurcharge,
                "deliveryDate": new_delivery.deliveryDate.strftime("%Y-%m-%d %H:%M:%S"),
                "uuid": new_delivery.uuid
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "code": 500,
            "message": "An error occurred while creating the delivery record.",
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
