FROM python:3.10-slim

# Set working directory in the container
WORKDIR /app

# Copy local code to the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 5300

# Command to run the app
CMD ["python", "settle_payment.py"]