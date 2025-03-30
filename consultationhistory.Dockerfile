# Use Python image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy app code
COPY requirements.txt requirements.txt
COPY consultationhistory.py /app/


# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 5000

# Start Flask app
CMD ["python", "consultationhistory.py"]