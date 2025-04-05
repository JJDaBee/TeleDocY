FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 4000

CMD ["uvicorn", "app.symptom_checker:app", "--host", "0.0.0.0", "--port", "4000"]
