from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from pydantic import BaseModel

app = Flask(__name__)
CORS(app)

# URLs of existing microservices
PATIENT_API_URL = "https://personal-gbst4bsa.outsystemscloud.com/PatientAPI/rest/patientAPI/patients"
CONSULTATION_HISTORY_URL = "http://consultation_history:5001/consultation_history"
SCHEDULE_URL = "http://schedule:5400/schedule"
DOCTOR_URL = "http://doctor:5500/doctor"
DYTE_API_URL = "http://create-token:5000/create-token"
NOTIFICATION_URL = "http://notification:5004/notification"

class ConsultationRequest(BaseModel):
    uuid: str
    reasonForVisit: str

def get_patient_info(uuid):
    try:
        response = requests.get(f"{PATIENT_API_URL}/{uuid}")
        response.raise_for_status()
        return response.json().get("patient", None)
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error fetching patient info: {e}")
        return None

def get_consultation_history(uuid):
    try:
        response = requests.get(f"{CONSULTATION_HISTORY_URL}/{uuid}")
        response.raise_for_status()
        return response.json().get("data", [])
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error fetching consultation history: {e}")
        return []

def get_available_doctor():
    try:
        response = requests.get(SCHEDULE_URL)
        response.raise_for_status()
        return response.json().get("data", None)
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error fetching available doctor: {e}")
        return None

def get_doctor_info(doctor_id):
    try:
        response = requests.get(f"{DOCTOR_URL}/{doctor_id}")
        response.raise_for_status()
        return response.json().get("data", None)
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error fetching doctor info: {e}")
        return None

def create_meeting(doctor_name, patient_uuid, reason_for_visit, meeting_id):
    try:
        payload = {"participantName": f"Patient-{patient_uuid}"}
        response = requests.post(DYTE_API_URL, json=payload)
        response.raise_for_status()
        
        meeting_data = response.json()
        return {
            "meeting_id": meeting_id,
            "auth_token": meeting_data.get("authToken")
        }
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error creating Dyte meeting: {e}")
        return None

def log_notification(patient_uuid, doctor_name, meeting_id):
    try:
        payload = {
            "patient_uuid": patient_uuid,
            "doctor_name": doctor_name,
            "meeting_id": meeting_id,
            "datetime": datetime.now().isoformat(),
            "status": "logged"
        }
        requests.post(NOTIFICATION_URL, json=payload)
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error logging notification: {e}")

@app.route("/book_consult", methods=["POST"])
def create_consult():
    try:
        data = request.get_json()
        req = ConsultationRequest(**data)

        # Step 1: Get patient info
        patient_data = get_patient_info(req.uuid)
        if not patient_data:
            return jsonify({"error": "Failed to fetch patient info"}), 400

        # Step 2: Get patient consultation history
        consultation_history = get_consultation_history(req.uuid)

        # Step 3: Query for available doctor
        doctor_info = get_available_doctor()
        if not doctor_info:
            return jsonify({"error": "No available doctors at the moment"}), 404

        doctor_id = doctor_info.get("doctorID")
        doctor_name = doctor_info.get("doctorName")
        meeting_id = doctor_info.get("meeting_id")

        # Step 4: Get doctor information using doctorID
        detailed_doctor_info = get_doctor_info(doctor_id)
        if not detailed_doctor_info:
            return jsonify({"error": "Failed to retrieve doctor details"}), 500

        # Step 5: Create a Dyte meeting auth token
        meeting_data = create_meeting(doctor_name, req.uuid, req.reasonForVisit, meeting_id)
        if not meeting_data:
            return jsonify({"error": "Failed to create meeting auth token"}), 500

        # Step 5.5: Log notification
        log_notification(req.uuid, doctor_name, meeting_id)

        # Step 6: Return successful response with details to the web app
        return jsonify({
            "message": "Consultation booked successfully",
            "doctor": doctor_name,
            "doctor_details": detailed_doctor_info,
            "meeting_id": meeting_id,
            "auth_token": meeting_data["auth_token"],
            "reason_for_visit": req.reasonForVisit
        })

    except Exception as e:
        app.logger.error(f"Unhandled exception: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)


