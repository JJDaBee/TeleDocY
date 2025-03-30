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

# Consumer microservice URL
CONSUMER_MICROSERVICE_URL = "http://localhost:8002/ask-ai"
OPENAI_MICROSERVICE_URL = "http://localhost:8001/generate"

# For Docker Testing !
# CONSUMER_MICROSERVICE_URL = "http://consumer-service:8002/ask-ai"
# OPENAI_MICROSERVICE_URL = "http://openai-service:8001/generate"

# Request model
class SearchQuery(BaseModel):
    query: str
    target_service: str = "consumer"  # Default to consumer service
    enhance_query: bool = True  # Whether to enhance the query or just tokenize

class TokenizationResponse(BaseModel):
    original_query: str
    tokenized_representation: list
    enhanced_query: str = None
    service_response: dict = None

@app.post("/tokenize")
def tokenize_query(data: SearchQuery):
    try:
        # Get the original query
        original_query = data.query
        
        # Tokenize with MiniLM (creates embeddings)
        embeddings = model.encode(original_query)
        
        # Basic query enhancement (can be expanded with more sophisticated NLP)
        enhanced_query = original_query
        if data.enhance_query:
            # Simple enhancement - add medical context if health-related terms are detected
            health_terms = ["pain", "ache", "symptom", "sick", "doctor", "headache", "fever", 
                           "cough", "runny", "nose", "stomach", "nausea", "vomiting"]
            
            if any(term in original_query.lower() for term in health_terms) and "medical context" not in original_query.lower():
                enhanced_query = f"In a medical context: {original_query}"
        
        # Create response object
        response = {
            "original_query": original_query,
            "tokenized_representation": embeddings.tolist(),  # Convert numpy array to list for JSON serialization
            "enhanced_query": enhanced_query
        }
        
        # Forward to appropriate service if requested
        if data.target_service:
            if data.target_service.lower() == "consumer":
                service_response = requests.post(
                    CONSUMER_MICROSERVICE_URL, 
                    json={"question": enhanced_query}
                )
                if service_response.status_code == 200:
                    response["service_response"] = service_response.json()
            elif data.target_service.lower() == "openai":
                service_response = requests.post(
                    OPENAI_MICROSERVICE_URL, 
                    json={"prompt": enhanced_query}
                )
                if service_response.status_code == 200:
                    response["service_response"] = service_response.json()
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)

# uvicorn minilm_tokenizer:app --host 0.0.0.0 --port 8003