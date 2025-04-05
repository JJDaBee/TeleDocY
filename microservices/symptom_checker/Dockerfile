FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 4000

CMD ["uvicorn", "symptom_checker:app.symptom_checker", "--host", "0.0.0.0", "--port", "4000"]
