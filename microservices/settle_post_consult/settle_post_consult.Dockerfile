# Use an official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY settle_post_consult.py .

# Expose port
EXPOSE 5200

# Run the application
CMD ["python", "settle_post_consult.py"]
