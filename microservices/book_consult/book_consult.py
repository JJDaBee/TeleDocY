from flask import Flask, request, jsonify
from flask_cors import CORS
from fastapi import FastAPI, HTTPException
from os import environ
from pydantic import BaseModel
import requests
import amqp_lib
from invokes import invoke_http


app = Flask(__name__)
CORS(app)
#URLs of existing microservices
PATIENT_API_URL = "https://personal-gbst4bsa.outsystemscloud.com/PatientAPI/rest/patientAPI/patients"
CONSULTATION_HISTORY_URL = "http://localhost:5000/consultation_history"
SCHEDULE_URL= "http://localhost:5400/schedule"
DYTE_API_URL= "http://localhost:5173/meeting"
NOTIFICATION_URL= "http://localhost:5300/notification"
ORDER_SERVICES_URL = "http://localhost:5600/order_services"

#Request model
class ConsultationRequest(BaseModel):
    uuid: str
    reasonForVisit: str

# RabbitMQ
rabbit_host = environ.get("rabbit_host") or "localhost"
rabbit_port = environ.get("rabbit_port") or 5672
exchange_name = environ.get("exchange_name") or "order_topic"
exchange_type = environ.get("exchange_type") or "topic"

connection = None 
channel = None

def connectAMQP():
    # Use global variables to reduce number of reconnection to RabbitMQ
    # There are better ways but this suffices for our lab
    global connection
    global channel

    print("  Connecting to AMQP broker...")
    try:
        connection, channel = amqp_lib.connect(
                hostname=rabbit_host,
                port=rabbit_port,
                exchange_name=exchange_name,
                exchange_type=exchange_type,
        )
    except Exception as exception:
        print(f"  Unable to connect to RabbitMQ.\n     {exception=}\n")
        exit(1) # terminate

@app.post("/book_consult")
def create_consult(data:ConsultationRequest):
    try:
        #1 Get patient info through uuid
        patient_response = requests.get(f"{PATIENT_API_URL}/{data.uuid}")
        if patient_response.status_code != 200:
            raise HTTPException(status_code=patient_response.status_code, detail="Failed to fetch patient info")
        patient_data = patient_response.json()["patient"]
        nric = patient_data["nric"]

        #2 Get patient consultation history 
        history_response = requests.get(f"{CONSULTATION_HISTORY_URL}/{patient_data['uuid']}")
        consultation_data = []
        if history_response.status_code == 200:
            consultation_data = history_response.json().get("data", [])
        
        #3 Query for available doctor
        doctor_response = requests.get(SCHEDULE_URL)
        if doctor_response.status_code == 200:
            doctor_info = doctor_response.json().get("data")
            doctor_name = doctor_info["doctorName"] if doctor_info else None

        if doctor_name:
            # Available doctor found
            print(f"Available doctor: {doctor_name}")
        else:
            raise HTTPException(status_code=404, detail="No available doctors at the moment.")
        
        #4 Get meeting id for zoom link for patient with uuid and doctor name from step 3
        dyte_response = request.post(DYTE_API_URL, json={
            "query": data.symptom_description, #need to tweak once know 
            "target_service": "consumer",
            "enhance_query": True
        })

        #5 Message patient Zoom link via AMQP(?)

        #6 Update consultation history (needs information put in by doctor)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
