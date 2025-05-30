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
    prescriptions = db.Column(db.JSON, nullable=False)
    deliveryDate = db.Column(db.DateTime, nullable=False)
    uuid = db.Column(db.String(20), nullable=False)

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
                "prescriptions": d.prescriptions,
                "deliveryDate": d.deliveryDate.strftime("%Y-%m-%d %H:%M:%S"),
                "uuid": d.uuid,
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

#@app.route("/delivery_detail/<int:deliveryID>")
#def get_delivery_surcharge(deliveryID):
#    delivery_detail = deliveryDetail.query.get(deliveryID)
#
#    if not delivery_detail:
#        return jsonify({
#            "code": 404,
#            "message": "Delivery record not found."
#        }), 404
#
#    return jsonify({
#        "code": 200,
#        "data": {
#            "deliverySurcharge": delivery_detail.deliverySurcharge,
#        }
#    }), 200

# ✅ POST a new delivery record
@app.route("/delivery_detail", methods=["POST"])
def create_delivery_detail():
    try:
        data = request.get_json()

        deliveryAddress = data.get("deliveryAddress")
        prescriptions = data.get("prescriptions")
        deliveryDate = data.get("deliveryDate")  # Optional
        uuid = data.get("uuid")

        if not (deliveryAddress and prescriptions and uuid):
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
            prescriptions=prescriptions,
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
                "prescriptions": new_delivery.prescriptions,
                "deliveryDate": new_delivery.deliveryDate.strftime("%Y-%m-%d %H:%M:%S"),
                "uuid": new_delivery.uuid,
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "code": 500,
            "message": "An error occurred while creating the delivery record.",
            "error": str(e)
        }), 500
    
@app.route("/delivery_detail/<int:deliveryID>", methods=["GET"])
def get_delivery_by_id(deliveryID):
    try:
        delivery = deliveryDetail.query.get(deliveryID)
        if not delivery:
            return jsonify({
                "code": 404,
                "message": f"Delivery with ID {deliveryID} not found."
            }), 404

        return jsonify({
            "code": 200,
            "data": {
                "deliveryID": delivery.deliveryID,
                "deliveryAddress": delivery.deliveryAddress,
                "prescriptions": delivery.prescriptions,
                "deliveryDate": delivery.deliveryDate.strftime("%Y-%m-%d %H:%M:%S"),
                "uuid": delivery.uuid
            }
        }), 200

    except Exception as e:
        return jsonify({
            "code": 500,
            "message": "An error occurred while fetching delivery details.",
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
