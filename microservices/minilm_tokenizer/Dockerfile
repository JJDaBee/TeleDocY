FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Pre-download MiniLM model to cache it in the image
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('paraphrase-MiniLM-L3-v2')

EXPOSE 4001

CMD ["uvicorn", "minilm_tokenizer:app", "--host", "0.0.0.0", "--port", "4001"]
