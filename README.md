# TeleDocY
# MiniLM Tokenizer + Fullstack App Setup

This guide walks you through setting up the `minilm_tokenizer` microservice and running the full app with Docker and Vite frontend.

---

## 1. Run the `minilm_tokenizer.py` Microservice Locally

1. Copy `minilm_tokenizer.py` into your project directory (same folder as this README).
2. Install the required dependencies:
   ```bash
   pip install fastapi uvicorn pydantic python-dotenv requests sentence-transformers tf-keras transformers==4.41.2
   ```
3. Start the microservice:
   ```bash
   uvicorn minilm_tokenizer:app --host 0.0.0.0 --port 4001
   ```

---

## 2. Run Backend Services via Docker

In the root of your GitHub project directory:

```bash
docker compose up --build -d
```

> This will build and start all backend microservices (e.g., delivery, notification, settle services) in detached mode.

---

## 3. Start the Vite Frontend

1. Move into the frontend directory:
   ```bash
   cd vite-project
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the Vite development server:
   ```bash
   npm run dev
   ```

Visit `http://localhost:5173` to see the app in action!