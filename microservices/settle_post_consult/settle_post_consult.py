from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

ORDER_URL = "http://order:5005/orders"
CONSULTATION_HISTORY_URL = "http://consultation_history:5001/consultation_history"
MEDICINE_INVENTORY_URL = "http://medicine_inventory:5002/medicine_inventory"

@app.route("/settle_post_consult", methods=["POST"])
def settle_post_consult():
    data = request.get_json()

    uuid = data.get("uuid")
    reasonForVisit = data.get("reasonForVisit")
    doctorName = data.get("doctorName")
    diagnosis = data.get("diagnosis")
    prescriptions = data.get("prescriptions")
    
    # 1️⃣ Create Order
    order_resp = requests.post(ORDER_URL, json={
        "uuid": uuid,
        "prescriptions": prescriptions,
        "prescriptionDate": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    })

    if order_resp.status_code != 201:
        return jsonify({"code": 500, "message": "Failed to create order", "details": order_resp.json()}), 500

    # 2️⃣ Create Consultation Record
    consultation_resp = requests.post(CONSULTATION_HISTORY_URL, json={
        "uuid": uuid,
        "dateTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "reasonForVisit": reasonForVisit,
        "doctorName": doctorName,
        "diagnosis": diagnosis,
        "prescriptions": prescriptions
    })

    if consultation_resp.status_code != 201:
        return jsonify({"code": 500, "message": "Failed to create consultation history", "details": consultation_resp.json()}), 500

    # 3️⃣ Reduce stock for each prescribed medicine
    reduction_results = []
    for item in prescriptions:
        medication = item.get("medicationName")
        quantity = item.get("quantity", 1)

        reduce_url = f"{MEDICINE_INVENTORY_URL}/{medication}/reduce"
        reduce_resp = requests.post(reduce_url, json={"quantity": quantity})

        if reduce_resp.status_code != 200:
            return jsonify({"code": 500, "message": f"Failed to reduce stock for {medication}", "details": reduce_resp.json()}), 500
        
        reduction_results.append(reduce_resp.json()["data"])

    return jsonify({
        "code": 200,
        "message": "Consultation settled successfully.",
        "data": {
            "uuid": uuid,
            "order": order_resp.json()["data"],
            "consultation": consultation_resp.json()["data"],
            "inventoryUpdates": reduction_results
        }
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5200, debug=True)
