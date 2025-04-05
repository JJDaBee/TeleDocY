# /app/main.py
import os
import sqlite3
import logging
from flask import Flask, request, jsonify
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
DB_PATH = "notifications.db"
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASS = os.getenv("GMAIL_PASS")

if not GMAIL_USER or not GMAIL_PASS:
    logging.warning("GMAIL_USER or GMAIL_PASS not set in environment variables")

def execute_sql_script(path):
    try:
        with sqlite3.connect(DB_PATH) as conn, open(path, 'r') as f:
            conn.executescript(f.read())
        logging.info("Executed SQL script successfully")
    except Exception as e:
        logging.error(f"Failed to execute SQL script: {e}")

def send_email(to_email, message):
    logging.info(f"Sending email to {to_email}")
    msg = MIMEText(message)
    msg['Subject'] = "Notification"
    msg['From'] = GMAIL_USER
    msg['To'] = to_email

    try:
        with SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(GMAIL_USER, GMAIL_PASS)
            server.send_message(msg)
        logging.info("Email sent successfully")
    except Exception as e:
        logging.error(f"Error sending email: {e}")
        raise

def log_notification(email, message):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("INSERT INTO notifications (email, message) VALUES (?, ?)", (email, message))
            conn.commit()
        logging.info("Notification logged to DB")
    except Exception as e:
        logging.error(f"Error logging notification: {e}")
        raise

@app.route("/notification/notify", methods=["POST"])
def notify():
    logging.info("/notification/notify called")
    data = request.get_json()

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON payload format"}), 400

    email = data.get("email")
    message = data.get("message")

    if not email or not message:
        logging.warning("Missing email or message in request")
        return jsonify({"error": "Missing email or message"}), 400

    try:
        send_email(email, message)
        log_notification(email, message)
        return jsonify({"status": "sent"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/notification/logs", methods=["GET"])
def get_logs():
    logging.info("/notification/logs called")
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, email, message, timestamp FROM notifications ORDER BY timestamp DESC")
            rows = cursor.fetchall()
            logs = [
                {"id": row[0], "email": row[1], "message": row[2], "timestamp": row[3]} for row in rows
            ]
        return jsonify(logs)
    except Exception as e:
        logging.error(f"Error fetching logs: {e}")
        return jsonify({"error": "Failed to retrieve logs"}), 500

if __name__ == "__main__":
    logging.info("Starting notification service on port 5004")
    execute_sql_script("notification.sql")
    app.run(host="0.0.0.0", port=5004)
