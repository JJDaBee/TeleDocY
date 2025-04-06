from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

ORDER_URL = "http://order:5005/orders"
CONSULT_HISTORY_URL = "http://consultationhistory:5001/consultation_history"
MEDICINE_INVENTORY_URL = "http://medicine_inventory:5002/medicine_inventory"

@app.route("/settle", methods=["POST"])
def settle_post_consult():
    data = request.get_json()
    uuid = data.get("uuid")
    reason_for_visit = data.get("reasonForVisit")
    doctor_name = data.get("doctorname")
    diagnosis = data.get("diagnosis")
    prescriptions = data.get("prescriptions")

    if not all([uuid, reason_for_visit, doctor_name, diagnosis, prescriptions]):
        return jsonify({"code": 400, "message": "Missing fields in request."}), 400

    # Step 1: Create order
    try:
        order_resp = requests.post(ORDER_URL, json={
            "uuid": uuid,
            "prescriptions": prescriptions
        }, timeout=5)

        if order_resp.status_code != 201:
            return jsonify({"code": 502, "message": "Failed to create order.", "details": order_resp.text}), 502
    except Exception as e:
        return jsonify({"code": 500, "message": "Error contacting order microservice.", "error": str(e)}), 500

    # Step 2: Create consultation history
    try:
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        consult_resp = requests.post(CONSULT_HISTORY_URL, json={
            "uuid": uuid,
            "dateTime": now,
            "reasonForVisit": reason_for_visit,
            "doctorName": doctor_name,
            "diagnosis": diagnosis,
            "prescriptions": prescriptions
        }, timeout=5)

        if consult_resp.status_code != 201:
            return jsonify({"code": 502, "message": "Failed to create consultation history.", "details": consult_resp.text}), 502
    except Exception as e:
        return jsonify({"code": 500, "message": "Error contacting consultation history microservice.", "error": str(e)}), 500

    # Step 3: Reduce inventory
    try:
        for item in prescriptions:
            medicine_name = item["medicineName"]
            quantity = item["quantity"]
            reduce_url = f"{MEDICINE_INVENTORY_URL}/{medicine_name}/reduce"

            reduce_resp = requests.post(reduce_url, json={"quantity": quantity}, timeout=5)

            if reduce_resp.status_code != 200:
                return jsonify({
                    "code": 502,
                    "message": f"Failed to reduce inventory for {medicine_name}",
                    "details": reduce_resp.text
                }), 502
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": "Error reducing medicine inventory.",
            "error": str(e)
        }), 500

    # ✅ Step 4: Fetch price and compile medicine inventory list
    medicine_inventory_list = []
    try:
        for item in prescriptions:
            medicine_name = item["medicineName"]
            quantity = item["quantity"]

            price_resp = requests.get(f"{MEDICINE_INVENTORY_URL}/{medicine_name}", timeout=5)

            if price_resp.status_code != 200:
                return jsonify({
                    "code": 502,
                    "message": f"Failed to get price for {medicine_name}",
                    "details": price_resp.text
                }), 502

            price_data = price_resp.json().get("data", {})
            medicine_inventory_list.append({
                "medicineName": medicine_name,
                "quantity": quantity,
                "price": price_data.get("price")
            })
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": "Error retrieving medicine prices.",
            "error": str(e)
        }), 500

    return jsonify({
        "code": 200,
        "message": "Successfully settled post consult.",
        "medicine_inventory_list": medicine_inventory_list
    }), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5200, debug=True)
