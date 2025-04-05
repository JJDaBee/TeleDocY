FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 4001

CMD ["uvicorn", "minilm_tokenizer:app", "--host", "0.0.0.0", "--port", "4001"]
