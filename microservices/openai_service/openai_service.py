from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

app = FastAPI()

# Initialize OpenAI Client with the API key from .env
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Request model
class RequestData(BaseModel):
    prompt: str
    model: str = "gpt-4o-mini" 

@app.post("/generate")
def generate_text(data: RequestData):
    try:
        response = client.chat.completions.create(
            model=data.model,
            messages=[{"role": "user", "content": data.prompt}]
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# uvicorn openai_microservice:app --host 0.0.0.0 --port 8001