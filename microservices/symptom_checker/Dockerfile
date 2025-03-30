# microservices/symptom_checker/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

CMD ["uvicorn", "app.symptom_checker:app", "--host", "0.0.0.0", "--port", "8000"]