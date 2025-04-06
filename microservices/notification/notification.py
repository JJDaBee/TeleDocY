import os
import logging
from flask import Flask, request, jsonify
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import time
import mysql.connector
from mysql.connector import Error
import pika
import threading
import json

def wait_for_mysql():
    retries = 10
    while retries > 0:
        try:
            conn = mysql.connector.connect(
                host="mysql",
                user="root",
                password="root"
            )
            if conn.is_connected():
                print("✅ MySQL is ready.")
                conn.close()
                break
        except Error as e:
            print(f"⏳ Waiting for MySQL: {e}")
            retries -= 1
            time.sleep(10)
    else:
        print("❌ MySQL never came online.")
        exit(1)

wait_for_mysql()

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# MySQL database config
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URI", "mysql+mysqlconnector://root:root@mysql:3306/notification")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Email credentials
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASS = os.getenv("GMAIL_PASS")

if not GMAIL_USER or not GMAIL_PASS:
    logging.warning("GMAIL_USER or GMAIL_PASS not set in environment variables")

# SQLAlchemy Model
class Notification(db.Model):
    __tablename__ = "notifications"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

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

# RabbitMQ Consumer Setup
def callback(ch, method, properties, body):
    try:
        data = json.loads(body)
        email = data.get("email")
        message = data.get("message")
        if email and message:
            send_email(email, message)
            with app.app_context():
                notification = Notification(email=email, message=message)
                db.session.add(notification)
                db.session.commit()
        else:
            logging.warning("Missing email or message in RabbitMQ payload.")
    except Exception as e:
        logging.error(f"Error processing RabbitMQ message: {e}")

def start_rabbitmq_consumer():
    def consume():
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
            channel = connection.channel()
            channel.queue_declare(queue='notification_queue', durable=True)
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue='notification_queue', on_message_callback=callback, auto_ack=True)
            logging.info("RabbitMQ consumer started. Waiting for messages...")
            channel.start_consuming()
        except Exception as e:
            logging.error(f"Failed to start RabbitMQ consumer: {e}")

    threading.Thread(target=consume, daemon=True).start()

start_rabbitmq_consumer()

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
        notification = Notification(email=email, message=message)
        db.session.add(notification)
        db.session.commit()
        return jsonify({"status": "sent"})
    except Exception as e:
        db.session.rollback()
        logging.error(f"Failed to send or log notification: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/notification/logs", methods=["GET"])
def get_logs():
    logging.info("/notification/logs called")
    try:
        logs = Notification.query.order_by(Notification.timestamp.desc()).all()
        return jsonify([
            {
                "id": n.id,
                "email": n.email,
                "message": n.message,
                "timestamp": n.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            } for n in logs
        ])
    except Exception as e:
        logging.error(f"Error fetching logs: {e}")
        return jsonify({"error": "Failed to retrieve logs"}), 500

if __name__ == "__main__":
    logging.info("Starting notification service on port 5004")
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5004)
