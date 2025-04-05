from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

PATIENT_API_URL = "https://personal-gbst4bsa.outsystemscloud.com/PatientAPI/rest/patientAPI/GetPatientByUUID"
CONSULT_HISTORY_URL_BASE = "http://consultationhistory:5001/consultation_history"
SCHEDULE_URL_BASE = "http://schedule:5006/schedule"


@app.route("/book_consult", methods=["POST"])
def book_consult():
    data = request.get_json()
    uuid = data.get("uuid")

    if not uuid:
        return jsonify({"code": 400, "message": "Missing 'uuid' in request."}), 400

    try:
        # Step 1: Call external Patient API
        patient_response = requests.post(PATIENT_API_URL, json={"uuid": uuid}, timeout=5)

        if patient_response.status_code != 200:
            return jsonify({
                "code": 502,
                "message": "Failed to fetch patient details from PatientAPI.",
                "status": patient_response.status_code,
                "details": patient_response.text
            }), 502

        patient_data = patient_response.json()

        # Step 2: Fetch consultation history
        history_url = f"{CONSULT_HISTORY_URL_BASE}/{uuid}"
        history_response = requests.get(history_url, timeout=5)

        if history_response.status_code != 200:
            return jsonify({
                "code": 502,
                "message": "Failed to fetch consultation history.",
                "status": history_response.status_code,
                "details": history_response.textx
            }), 502

        consult_history = history_response.json()

        return jsonify({
            "code": 200,
            "message": "Successfully fetched patient and consultation history.",
            "patient": patient_data,
            "consultation_history": consult_history.get("data", [])
        }), 200

    except requests.RequestException as e:
        return jsonify({
            "code": 500,
            "message": "Error during service orchestration.",
            "error": str(e)
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5100, debug=True)