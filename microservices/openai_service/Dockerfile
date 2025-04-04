FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 4002

CMD ["uvicorn", "openai_service:app", "--host", "0.0.0.0", "--port", "4002"]
