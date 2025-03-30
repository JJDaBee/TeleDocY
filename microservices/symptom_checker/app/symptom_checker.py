from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"] for stricter security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# URLs of your existing microservices
PATIENT_API_URL = "https://personal-gbst4bsa.outsystemscloud.com/PatientAPI/rest/patientAPI/patients"
CONSULTATION_HISTORY_URL = "http://localhost:5000/consultation_history"
MINILM_TOKENIZER_URL = "http://localhost:8003/tokenize"


# Request model
class SymptomCheckRequest(BaseModel):
    uuid: str
    symptom_description: str

@app.post("/check-symptoms")
def check_symptoms(data: SymptomCheckRequest):
    try:
        # Step 1: Fetch Patient Info
        patient_response = requests.get(f"{PATIENT_API_URL}/{data.uuid}")
        if patient_response.status_code != 200:
            raise HTTPException(status_code=patient_response.status_code, detail="Failed to fetch patient info")
        print(patient_response.json())
        patient_data = patient_response.json()["patient"]
        nric = patient_data["nric"]

        # Step 2: Fetch Consultation History
        history_response = requests.get(f"{CONSULTATION_HISTORY_URL}/{patient_data['uuid']}")
        consultation_data = []
        if history_response.status_code == 200:
            consultation_data = history_response.json().get("data", [])

        # Step 3: Tokenize & Enhance Query via MiniLM
        tokenizer_response = requests.post(MINILM_TOKENIZER_URL, json={
            "query": data.symptom_description,
            "target_service": "consumer",
            "enhance_query": True
        })
        if tokenizer_response.status_code != 200:
            raise HTTPException(status_code=tokenizer_response.status_code, detail="Failed during tokenization")
        tokenizer_data = tokenizer_response.json()

        # Step 4: Combine all into one response
        return {
            "patient_info": patient_data,
            "consultation_history": consultation_data,
            "enhanced_query": tokenizer_data.get("enhanced_query"),
            "ai_response": tokenizer_data.get("service_response", {}).get("response")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run with:
# uvicorn symptom_checker:app --host 0.0.0.0 --port 8000

####################################################################3

# import requests

# response = requests.post("http://localhost:8002/ask-ai", json={"question": "Explain AI in 3 sentences"})
# print(response.json())

# C:\wamp64\www\GitHub\TeleDocY\microservices>curl -X POST http://localhost:8000/check-symptoms -H "Content-Type: application/json" -d "{\"uuid\":\"uuid-9300\", \"symptom_description\":\"Am I having a heart attack?\"}"