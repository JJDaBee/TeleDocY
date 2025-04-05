from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

app = FastAPI()

# Initialize OpenAI Client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Request model
class RequestData(BaseModel):
    prompt: str
    model: str = "gpt-4o-mini"

@app.post("/generate")
def generate_text(data: RequestData):
    try:
        print("📥 Received prompt:", data.prompt)
        print("🤖 Using model:", data.model)

        response = client.chat.completions.create(
            model=data.model,
            messages=[{"role": "user", "content": data.prompt}]
        )
        result = response.choices[0].message.content
        print("✅ OpenAI generated response:", result)

        return {"response": result}

    except Exception as e:
        print("❌ Error during OpenAI completion:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "openai_microservice"}

# Run with:
# uvicorn openai_service:app --host 0.0.0.0 --port 4002
