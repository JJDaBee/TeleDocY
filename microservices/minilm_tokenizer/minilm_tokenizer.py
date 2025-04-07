import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import requests
from dotenv import load_dotenv

app = FastAPI()

# Load environment variables
load_dotenv()

# Initialize the SentenceTransformer model (MiniLM)
print("🔧 Loading MiniLM model...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("✅ MiniLM model loaded.")

# OpenAI service URL (uncomment or load from .env)
SYMPTOMCHECKER = os.getenv("SYMPTOMCHECKER", "http://localhost:4000/check-symptoms")

# Request model
class SearchQuery(BaseModel):
    query: str
    target_service: str = "consumer"  # Default to consumer service
    enhance_query: bool = True        # Whether to enhance the query or just tokenize

class TokenizationResponse(BaseModel):
    original_query: str
    tokenized_representation: list
    enhanced_query: str = None
    service_response: dict = None

@app.post("/tokenize")
def tokenize_query(data: SearchQuery):
    try:
        print("📥 Received query:", data.query)
        
        # Step 1: Tokenize with MiniLM (creates embeddings)
        print("🔍 Generating embeddings using MiniLM...")
        embeddings = model.encode(data.query)
        print("✅ Embeddings generated.")

        # Step 2: Enhance query (if applicable)
        enhanced_query = data.query
        if data.enhance_query:
            health_terms = [
                "pain", "ache", "symptom", "sick", "doctor", "headache", "fever", 
                "cough", "runny", "nose", "stomach", "nausea", "vomiting"
            ]
            if any(term in data.query.lower() for term in health_terms) and "medical context" not in data.query.lower():
                enhanced_query = f"In a medical context: {data.query}"
                print("🧠 Enhanced query applied:", enhanced_query)
            else:
                print("ℹ️ No enhancement needed.")

        # Step 3: Construct response so far
        response = {
            "original_query": data.query,
            "tokenized_representation": embeddings.tolist(),
            "enhanced_query": enhanced_query
        }

        # Step 4: Optionally query OpenAI microservice
        if data.target_service.lower() in ["consumer", "openai"]:
            print("🤖 Forwarding to OpenAI microservice:", SYMPTOMCHECKER)
            prompt = enhanced_query
            model_to_use = "gpt-4o-mini"

            openai_payload = {"prompt": prompt, "model": model_to_use}
            print("📤 Payload:", openai_payload)

            openai_response = requests.post(SYMPTOMCHECKER, json=openai_payload)

            if openai_response.status_code == 200:
                print("✅ OpenAI microservice responded successfully.")
                response["service_response"] = openai_response.json()
            else:
                print("❌ Failed to contact OpenAI microservice. Status:", openai_response.status_code)
                response["service_response"] = {
                    "error": f"Failed to reach OpenAI microservice. Status: {openai_response.status_code}",
                    "details": openai_response.text
                }

        print("📦 Final response payload:")
        print(json.dumps(response, indent=2))  # Pretty print full response for logs

        return response

    except Exception as e:
        print("❌ Exception occurred in /tokenize endpoint")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# Health check endpoint (optional for readiness probe)
@app.get("/health")
def health_check():
    return {"status": "ok", "model": "MiniLM loaded"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4001)

# Command to run: uvicorn minilm_tokenizer:app --host 0.0.0.0 --port 4001

# INFO:     127.0.0.1:54674 - "POST /tokenize HTTP/1.1" 200 OK
# INFO:     Shutting down
# INFO:     Waiting for application shutdown.
# INFO:     Application shutdown complete.
# INFO:     Finished server process [2736]
# PS C:\wamp64\www\ESD\minilm_openai> uvicorn minilm_tokenizer:app --host 0.0.0.0 --port 4001
