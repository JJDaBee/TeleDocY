from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import pika
import sys, os
from os import environ
from pydantic import BaseModel

#import amqp_lib
from invokes import invoke_http

app = Flask(__name__)

#URLs of existing microservices
PATIENT_API_URL = "https://personal-gbst4bsa.outsystemscloud.com/PatientAPI/rest/patientAPI/patients"
CONSULTATION_HISTORY_URL = "http://localhost:5000/consultation_history"
SCHEDULE_URL= "http://localhost:5400/schedule"
#DYTE_API_URL= some link
NOTIFICATION_URL= "http://localhost:5300/notification"
ORDER_SERVICES_URL = "http://localhost:5600/order_services"

CORS(app)