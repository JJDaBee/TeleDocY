from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Configuration
PAYMENT_SERVICE_URL = "http://payment:5009/payments"
PATIENT_ADDRESS_URL = "https://personal-gbst4bsa.outsystemscloud.com/PatientAPI/rest/patientAPI/GetPatientAddress"
STRIPE_PAYMENT_URL = "http://stripe-wrapper:3001/create-checkout"
DELIVERY_DETAIL_URL = "http://delivery_detail:5003/delivery_detail"

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
        patient_data = address_json.get("Patient", {})
        patient_address = patient_data.get("Address", "Address not found")
        patient_name = f"{patient_data.get('FirstName', '')} {patient_data.get('LastName', '')}".strip()

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
            "deliveryAddress": patient_address,  # from Step 1
            "prescriptions": payment_data.get("prescriptions", []),  # from Step 2
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
