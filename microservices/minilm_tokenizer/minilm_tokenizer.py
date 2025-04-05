import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import requests
from dotenv import load_dotenv

app = FastAPI()

# Load environment variables
load_dotenv()

# Initialize the SentenceTransformer model (MiniLM)
model = SentenceTransformer('all-MiniLM-L6-v2')

# OpenAI microservice URL
OPENAI_MICROSERVICE_URL = "http://localhost:4002/generate"

# Request model
class SearchQuery(BaseModel):
    query: str
    target_service: str = "openai"  # Default to OpenAI service
    enhance_query: bool = True      # Whether to enhance the query or just tokenize

class TokenizationResponse(BaseModel):
    original_query: str
    tokenized_representation: list
    enhanced_query: str = None
    service_response: dict = None

@app.post("/tokenize")
def tokenize_query(data: SearchQuery):
    try:
        # Step 1: Get the original query
        original_query = data.query

        # Step 2: Tokenize with MiniLM (creates embeddings)
        embeddings = model.encode(original_query)

        # Step 3: Basic query enhancement
        enhanced_query = original_query
        if data.enhance_query:
            health_terms = [
                "pain", "ache", "symptom", "sick", "doctor", "headache", "fever", 
                "cough", "runny", "nose", "stomach", "nausea", "vomiting"
            ]
            if any(term in original_query.lower() for term in health_terms) and "medical context" not in original_query.lower():
                enhanced_query = f"In a medical context: {original_query}"

        # Step 4: Create base response
        response = {
            "original_query": original_query,
            "tokenized_representation": embeddings.tolist(),
            "enhanced_query": enhanced_query
        }

        # Step 5: Forward enhanced query to OpenAI
        service_response = requests.post(
            OPENAI_MICROSERVICE_URL,
            json={"prompt": enhanced_query}
        )
        if service_response.status_code == 200:
            response["service_response"] = service_response.json()
        else:
            response["service_response"] = {
                "error": f"OpenAI service failed with status {service_response.status_code}"
            }

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4001)
