from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import subprocess
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI','mysql+mysqlconnector://root:root@mysql:3306/deliveryDetail')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

class deliveryDetail(db.Model):
    __tablename__ = "deliveryDetail"

    deliveryAddress = db.Column(db.String(1000),primary_key=True, nullable=False)
    medication = db.Column(db.String(1000), nullable=False)
    deliverySurcharge = db.Column(db.Integer, nullable=False)
    deliveryDate = db.Column(db.DateTime,primary_key=True, nullable=False)

@app.route("/order/delivery_detail/<string:deliveryAddress>")

def get_delivery_surcharge(deliveryAddress):
    # Query the database to find the delivery details based on delivery address
    delivery_detail = deliveryDetail.query.filter_by(deliveryAddress=deliveryAddress).first()
    
    # Check if the delivery address exists in the database
    if not delivery_detail:
        return jsonify({
            "code": 404,
            "message": "Delivery address not found."
        }), 404
    
    # Return the delivery surcharge
    return jsonify({
        "code": 200,
        "data": {
            "deliverySurcharge": delivery_detail.deliverySurcharge,
        }
    }), 200

if __name__ == '__main__':
    app.run(port=5200, debug=True)