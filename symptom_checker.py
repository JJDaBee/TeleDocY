import requests

response = requests.post("http://localhost:8002/ask-ai", json={"question": "Explain AI in 3 sentences"})
print(response.json())

#curl -X POST "http://localhost:8001/generate" -H "Content-Type: application/json" -d "{\"prompt\": \"Write a haiku about AI\"}"
