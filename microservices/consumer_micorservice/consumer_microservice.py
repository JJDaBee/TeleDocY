import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Request model
class QueryData(BaseModel):
    question: str

OPENAI_MICROSERVICE_URL = "http://localhost:8001/generate"

# Docker Testing !
# OPENAI_MICROSERVICE_URL = "http://openai-service:8001/generate"

@app.post("/ask-ai")
def ask_ai(data: QueryData):
    try:
        response = requests.post(OPENAI_MICROSERVICE_URL, json={"prompt": data.question})
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# uvicorn consumer_microservice:app --host 0.0.0.0 --port 8002