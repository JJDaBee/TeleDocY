from flask import Flask, request, jsonify
import requests
from datetime import datetime
import pika
import json

app = Flask(__name__)

ORDER_URL = "http://order:5005/orders"
CONSULT_HISTORY_URL = "http://consultationhistory:5001/consultation_history"
MEDICINE_INVENTORY_URL = "http://medicine_inventory:5002/medicine_inventory"
PAYMENT_URL = "http://payment:5009/payments"
PATIENT_API_URL = "https://personal-gbst4bsa.outsystemscloud.com/PatientAPI/rest/patientAPI/GetPatientByUUID"
OPENAI_URL = "http://openai_service:4002/"

def format_summary_string(firstname, payment, prescriptions):
    prescription_lines = [
        f"- {p['medicineName']} ({p['dosage']}), Qty: {p['quantity']}" for p in prescriptions
    ]
    prescriptions_str = "\n".join(prescription_lines)
    summary = (
        f"Consultation Summary for {firstname}:\n\n"
        f"Prescriptions:\n{prescriptions_str}\n\n"
        f"Payment Details:\n"
        f"Amount: ${payment.get('amount'):.2f}\n"
        f"Datetime: {payment.get('datetime')}\n"
        f"Payment ID: {payment.get('paymentID')}"
    )
    return summary

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
        print(f"❌ Failed to publish message to RabbitMQ: {e}")

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

    try:
        order_resp = requests.post(ORDER_URL, json={"uuid": uuid, "prescriptions": prescriptions}, timeout=5)
        if order_resp.status_code != 201:
            return jsonify({"code": 502, "message": "Failed to create order.", "details": order_resp.text}), 502
    except Exception as e:
        return jsonify({"code": 500, "message": "Error contacting order microservice.", "error": str(e)}), 500

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

    medicine_inventory_list = []
    try:
        for item in prescriptions:
            medicine_name = item["medicineName"]
            quantity = item["quantity"]
            reduce_url = f"{MEDICINE_INVENTORY_URL}/{medicine_name}/reduce"
            reduce_resp = requests.post(reduce_url, json={"quantity": quantity}, timeout=5)
            if reduce_resp.status_code != 200:
                return jsonify({"code": 502, "message": f"Failed to reduce inventory for {medicine_name}", "details": reduce_resp.text}), 502
            price_resp = requests.get(f"{MEDICINE_INVENTORY_URL}/{medicine_name}", timeout=5)
            price_data = price_resp.json().get("data", {})
            medicine_inventory_list.append({"medicineName": medicine_name, "quantity": quantity, "price": price_data.get("price")})
    except Exception as e:
        return jsonify({"code": 500, "message": "Error processing medicine inventory.", "error": str(e)}), 500

    payment_payload = {
        "uuid": uuid,
        "medicine_inventory_list": medicine_inventory_list,
        "prescriptions": prescriptions
    }

    created_payment = {}
    try:
        payment_response = requests.post(PAYMENT_URL, json=payment_payload, timeout=5)
        if payment_response.status_code != 201:
            return jsonify({"code": 502, "message": "Failed to create payment.", "details": payment_response.text}), 502
        created_payment = payment_response.json().get("data", {})
    except Exception as e:
        return jsonify({"code": 500, "message": "Error contacting payment microservice.", "error": str(e)}), 500

    try:
        patient_resp = requests.post(PATIENT_API_URL, json={"uuid": uuid}, timeout=5)
        patient_data = patient_resp.json()
        patient_info = patient_data.get("patient", {})
        firstname = patient_info.get("FirstName", "Patient")
        email = patient_info.get("Email", "test@example.com")
        summary_string = format_summary_string(firstname, created_payment, prescriptions)
    except Exception as e:
        summary_string = f"Could not generate summary: {str(e)}"
        email = "test@example.com"

    openai_response = ""
    try:
        ai_resp = requests.post(f"{OPENAI_URL}/generate", json={"prompt": summary_string})
        if ai_resp.status_code == 200:
            openai_response = ai_resp.json().get("response", "")
        else:
            openai_response = f"OpenAI error: {ai_resp.status_code} - {ai_resp.text}"
    except Exception as e:
        openai_response = f"Error contacting OpenAI service: {str(e)}"

    try:
        send_notification_via_amqp(email, openai_response)
    except Exception as e:
        print(f"❌ Notification error: {str(e)}")

    return jsonify({
        "code": 200,
        "message": "Post-consultation process completed successfully.",
        "medicines": medicine_inventory_list,
        "payment": created_payment,
        "summary": summary_string,
        "openai_response": openai_response
    }), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5200, debug=True)