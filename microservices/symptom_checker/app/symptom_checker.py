from fastapi.middleware.cors import CORSMiddleware # type: ignore
from fastapi import FastAPI, HTTPException # type: ignore
from pydantic import BaseModel
import requests
import traceback

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
CONSULTATION_HISTORY_URL = "http://consultationhistory:5001/consultation_history"
MINILM_TOKENIZER_URL = "http://host.docker.internal:4001/tokenize"


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
        patient_data = patient_response.json()["patient"]
        nric = patient_data["nric"]
        print("👤 Patient NRIC:", patient_data.get("nric"))
        
        # Step 2: Fetch Consultation History
        history_response = requests.get(f"{CONSULTATION_HISTORY_URL}/{data.uuid}")
        print("✅ Consultation history API status code:", history_response.status_code)
        consultation_data = []
        if history_response.status_code == 200:
            consultation_data = history_response.json().get("data", [])

       # Step 3: Tokenize & Enhance Query via MiniLM
        print("🤖 [Step 3] Sending symptom description to tokenizer microservice")
        tokenizer_request_payload = {
            "query": data.symptom_description,
            "target_service": "openai",
            "enhance_query": True
        }
        print("📝 Tokenizer request payload:", tokenizer_request_payload)

        tokenizer_response = requests.post(MINILM_TOKENIZER_URL, json=tokenizer_request_payload)

        print("✅ Tokenizer API status code:", tokenizer_response.status_code)
        if tokenizer_response.status_code != 200:
            raise HTTPException(status_code=tokenizer_response.status_code, detail="Failed during tokenization")

        tokenizer_data = tokenizer_response.json()
        print("🧠 Tokenizer response:", tokenizer_data)

        # Step 4: Forward enhanced query to OpenAI microservice
        OPENAI_MICROSERVICE_URL = "http://host.docker.internal:4002/generate"  
        enhanced_query = tokenizer_data.get("enhanced_query")
        print("📤 Forwarding enhanced query to OpenAI microservice...")

        openai_payload = {
            "prompt": enhanced_query,
            "model": "gpt-4o-mini"
        }
        print("📝 OpenAI request payload:", openai_payload)

        openai_response = requests.post(OPENAI_MICROSERVICE_URL, json=openai_payload)

        print("✅ OpenAI API status code:", openai_response.status_code)
        if openai_response.status_code != 200:
            raise HTTPException(status_code=openai_response.status_code, detail="Failed to get OpenAI response")

        ai_result = openai_response.json()
        print("🤖 OpenAI response:", ai_result)

        return {
            "patient_info": patient_data,
            "consultation_history": consultation_data,
            "enhanced_query": enhanced_query,
            "ai_response": ai_result.get("response")
        }


    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# Run with:
# uvicorn symptom_checker:app --host 0.0.0.0 --port 4000

####################################################################
