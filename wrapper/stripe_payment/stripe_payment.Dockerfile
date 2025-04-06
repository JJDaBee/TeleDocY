# Dockerfile
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy app files
COPY stripe_payment.py /app/
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (same as used in app.py)
EXPOSE 3001

# Run the app
CMD ["python", "stripe_payment.py"]
