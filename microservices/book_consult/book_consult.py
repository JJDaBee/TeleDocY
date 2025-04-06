from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

PATIENT_API_URL = "https://personal-gbst4bsa.outsystemscloud.com/PatientAPI/rest/patientAPI/GetPatientByUUID"
CONSULT_HISTORY_URL_BASE = "http://consultationhistory:5001/consultation_history"
SCHEDULE_URL_BASE = "http://schedule:5006/schedule"
DOCTOR_URL_BASE = "http://doctor:5007/doctor"
DYTE_WRAPPER_URL = "http://dyte-wrapper:5000/create-token"

@app.route("/book_consult", methods=["POST"])
def book_consult():
    data = request.get_json()
    uuid = data.get("uuid")

    if not uuid:
        return jsonify({"code": 400, "message": "Missing 'uuid' in request."}), 400

    try:
        # Step 1: Patient API
        patient_response = requests.post(PATIENT_API_URL, json={"uuid": uuid}, timeout=5)
        if patient_response.status_code != 200:
            return jsonify({"code": 502, "message": "Failed to fetch patient details."}), 502
        patient_data = patient_response.json()

        # Step 2: Consultation history
        history_response = requests.get(f"{CONSULT_HISTORY_URL_BASE}/{uuid}", timeout=5)
        if history_response.status_code != 200:
            return jsonify({"code": 502, "message": "Failed to fetch consultation history."}), 502
        consult_history = history_response.json().get("data", [])

        # Step 3: Schedule microservice
        schedule_response = requests.get(SCHEDULE_URL_BASE, timeout=5)
        if schedule_response.status_code != 200:
            return jsonify({"code": 502, "message": "Failed to fetch available doctor."}), 502
        assigned_doctor = schedule_response.json().get("data", {})
        doctor_name = assigned_doctor.get("doctorName")
        meeting_id = assigned_doctor.get("roomid")

        if not doctor_name or not meeting_id:
            return jsonify({"code": 502, "message": "Missing doctorName or roomid in schedule response."}), 502

        # Step 4: Doctor profile
        doctor_response = requests.get(f"{DOCTOR_URL_BASE}/{doctor_name}", timeout=5)
        if doctor_response.status_code != 200:
            return jsonify({"code": 502, "message": "Failed to fetch doctor profile."}), 502
        doctor_profile = doctor_response.json().get("data", {})

        # ✅ Step 5: Dyte wrapper to generate auth token
        participant_name = patient_data.get("name", "Patient")
        dyte_response = requests.post(DYTE_WRAPPER_URL, json={
            "participantName": participant_name,
            "meetingId": meeting_id
        }, timeout=5)

        if dyte_response.status_code != 200:
            return jsonify({
                "code": 502,
                "message": "Failed to generate Dyte auth token.",
                "details": dyte_response.text
            }), 502

        dyte_token = dyte_response.json().get("authToken")

        return jsonify({
            "code": 200,
            "message": "Successfully booked consult details.",
            "patient": patient_data,
            "consultation_history": consult_history,
            "assigned_doctor": assigned_doctor,
            "doctor_profile": doctor_profile,
            "dyte_token": dyte_token
        }), 200

    except requests.RequestException as e:
        return jsonify({
            "code": 500,
            "message": "Error during service orchestration.",
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5100, debug=True)
