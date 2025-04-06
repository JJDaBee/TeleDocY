from flask import Flask, request, jsonify
import requests
import pika
import json
from flask_cors import CORS 

app = Flask(__name__)
CORS(app)

# Configuration
PAYMENT_SERVICE_URL = "http://payment:5009/payments"
PATIENT_ADDRESS_URL = "https://personal-gbst4bsa.outsystemscloud.com/PatientAPI/rest/patientAPI/GetPatientAddress"
PATIENT_DETAIL_URL = "https://personal-gbst4bsa.outsystemscloud.com/PatientAPI/rest/patientAPI/GetPatientByUUID"
STRIPE_PAYMENT_URL = "http://stripe-wrapper:3001/create-checkout"
DELIVERY_DETAIL_URL = "http://delivery_detail:5003/delivery_detail"

def send_notification_via_amqp(email, message):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        channel = connection.channel()
        channel.queue_declare(queue='notification_queue', durable=True)
        channel.basic_publish(
            exchange='',
            routing_key='notification_queue',
            body=json.dumps({"email": email, "message": message}),
            properties=pika.BasicProperties(delivery_mode=2)
        )
        connection.close()
    except Exception as e:
        print(f"❌ Failed to publish delivery notification: {e}")

@app.route("/settle_payment", methods=["POST"])
def settle_payment():
    data = request.get_json()
    payment_id = data.get("paymentID")
    uuid = data.get("uuid")

    if not payment_id or not uuid:
        return jsonify({
            "code": 400,
            "message": "Missing 'paymentID' or 'uuid'."
        }), 400

    try:
        # ✅ Step 1: Get patient address and name
        address_response = requests.post(PATIENT_ADDRESS_URL, json={"uuid": uuid}, timeout=5)
        if address_response.status_code != 200:
            return jsonify({
                "code": 502,
                "message": "Failed to retrieve patient address.",
                "details": address_response.text
            }), 502

        address_json = address_response.json()
        patient_address = address_json.get("Patient", {}).get("Address", "Address not found")

        # ✅ Step 1b: Get patient name and email from UUID
        detail_response = requests.post(PATIENT_DETAIL_URL, json={"uuid": uuid}, timeout=5)
        if detail_response.status_code != 200:
            return jsonify({
                "code": 502,
                "message": "Failed to retrieve patient details.",
                "details": detail_response.text
            }), 502

        detail_data = detail_response.json().get("patient", {})
        patient_name = f"{detail_data.get('FirstName', '')} {detail_data.get('LastName', '')}".strip()
        patient_email = detail_data.get("Email", "test@example.com")

        # ✅ Step 2: Get payment details
        response = requests.get(f"{PAYMENT_SERVICE_URL}/{payment_id}", timeout=5)
        if response.status_code != 200:
            return jsonify({
                "code": 502,
                "message": f"Failed to fetch payment with ID {payment_id}",
                "details": response.text
            }), 502

        payment_data = response.json().get("data", {})
        amount_in_cents = int(payment_data["amount"] * 100)
        description = f"Payment for {patient_name} (Payment ID: {payment_id})"

        # ✅ Step 3: Create Stripe Checkout Session
        stripe_payload = {
            "amount": amount_in_cents,
            "description": description
        }

        stripe_response = requests.post(STRIPE_PAYMENT_URL, json=stripe_payload, timeout=10)
        if stripe_response.status_code != 200:
            return jsonify({
                "code": 502,
                "message": "Failed to create Stripe checkout session.",
                "details": stripe_response.text
            }), 502

        stripe_checkout_url = stripe_response.json().get("url")

        # ✅ Step 4: Create Delivery Record
        delivery_payload = {
            "deliveryAddress": patient_address,
            "prescriptions": payment_data.get("prescriptions", []),
            "uuid": uuid
        }

        delivery_response = requests.post(DELIVERY_DETAIL_URL, json=delivery_payload, timeout=10)
        if delivery_response.status_code != 201:
            return jsonify({
                "code": 502,
                "message": "Failed to create delivery record.",
                "details": delivery_response.text
            }), 502

        delivery_data = delivery_response.json().get("data", {})

        # ✅ Step 5: Notify patient via RabbitMQ
        delivery_summary = (
            f"Hi {patient_name},\n\n"
            f"Your delivery has been scheduled successfully to the following address:\n"
            f"{patient_address}\n\n"
            f"Delivery Date: {delivery_data.get('deliveryDate', 'TBD')}\n"
            f"Prescriptions:\n"
            + "\n".join([f"- {p['medicineName']} (Qty: {p['quantity']})" for p in delivery_payload["prescriptions"]])
        )

        send_notification_via_amqp(patient_email, delivery_summary)

        # ✅ Final Response
        return jsonify({
            "code": 200,
            "message": "Successfully processed settle_payment.",
            "patient_name": patient_name,
            "patient_address": patient_address,
            "payment": payment_data,
            "stripe_checkout_url": stripe_checkout_url,
            "delivery": delivery_data  
        }), 200

    except requests.RequestException as e:
        return jsonify({
            "code": 500,
            "message": "Error communicating with external services.",
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5300, debug=True)