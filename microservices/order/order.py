from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DB_URI', 'mysql+mysqlconnector://root:root@mysql:3306/order'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

class Order(db.Model):
    __tablename__ = 'order'
    
    orderID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.String(36), nullable=False)
    medicines = db.Column(db.JSON, nullable=False)
    prescriptionDate = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "orderID": self.orderID,
            "uuid": self.uuid,
            "medicines": self.medicines,
            "prescriptionDate": self.prescriptionDate.strftime("%Y-%m-%d %H:%M:%S")
        }

# GET all orders
@app.route("/orders", methods=["GET"])
def get_all_orders():
    orders = Order.query.all()
    return jsonify({
        "code": 200,
        "data": [order.to_dict() for order in orders]
    }), 200

# POST new order
@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()
    uuid = data.get("uuid")
    medicines = data.get("medicines")

    if not uuid or not medicines:
        return jsonify({
            "code": 400,
            "message": "Missing 'uuid' or 'medicines'."
        }), 400

    try:
        new_order = Order(uuid=uuid, medicines=medicines)
        db.session.add(new_order)
        db.session.commit()

        return jsonify({
            "code": 201,
            "message": "Order created successfully.",
            "data": new_order.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "code": 500,
            "message": "An error occurred while creating the order.",
            "error": str(e)
        }), 500
    
# GET order by orderID
@app.route("/orders/<int:orderID>", methods=["GET"])
def get_order_by_id(orderID):
    order = Order.query.get(orderID)

    if order:
        return jsonify({
            "code": 200,
            "data": order.to_dict()
        }), 200
    else:
        return jsonify({
            "code": 404,
            "message": f"Order with ID {orderID} not found."
        }), 404
    
# GET all orders by patient UUID
@app.route("/orders/uuid/<string:uuid>", methods=["GET"])
def get_orders_by_uuid(uuid):
    orders = Order.query.filter_by(uuid=uuid).all()

    if orders:
        return jsonify({
            "code": 200,
            "data": [order.to_dict() for order in orders]
        }), 200
    else:
        return jsonify({
            "code": 404,
            "message": f"No orders found for patient with UUID: {uuid}"
        }), 404

# DELETE order by orderID
@app.route("/orders/<int:orderID>", methods=["DELETE"])
def delete_order(orderID):
    order = Order.query.get(orderID)

    if order:
        db.session.delete(order)
        db.session.commit()
        return jsonify({
            "code": 200,
            "message": f"Order with ID {orderID} deleted successfully."
        }), 200
    else:
        return jsonify({
            "code": 404,
            "message": f"Order with ID {orderID} not found."
        }), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)
