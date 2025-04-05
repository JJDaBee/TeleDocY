# Use Python image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy app code
COPY requirements.txt requirements.txt
COPY consultation_history.py /app/


# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 5001

# Start Flask app
CMD ["python", "consultation_history.py"]