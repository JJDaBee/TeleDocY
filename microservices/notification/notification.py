#just to store notification logs w/ status

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
import os
import subprocess
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI','mysql+mysqlconnector://root:root@localhost:3306/notification') #rmb to change name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)
project_root = os.path.dirname(os.path.abspath(__file__))
init_path = os.path.join(project_root, "microservices/notification", "notification.sql")

class notification(db.Model):
    __tablename__ = "notification"

    uuid=db.Column(db.String(20), primary_key = True)
    notificationLog=db.Column(db.String(1000),nullable=False)
    dateTime=db.Column(db.DateTime,nullable=False)
    status=db.Column(db.String(100),nullable=False)


@app.route("/notification", methods=["POST"])
def create_notificationrecord():
    data = request.get_json()
    uuid=data.get("uuid")
    dateTime = data.get("dateTime")
    notificationLog=data.get("notificationLog")
    status=data.get("status")

    new_notification = notification(
        uuid=uuid,
        dateTime=dateTime,
        notificationLog=notificationLog,
        status=status 
    )
    try:
        # Add the new consultation to the session and commit to the database
        db.session.add(new_notification)
        db.session.commit()
        result =subprocess.run([
            "docker", "exec", "-i", "teledocy-mysql-1",  # use your container name
            "mysqldump", "-u", "root", "-proot", "notification"
        ], stdout=open(init_path, "w"))
        print("mysqldump executed. Return code:", result.returncode)
        return jsonify({
            "code": 201,
            "message": "Notification record created successfully.",
            "data": {
                "uuid" : new_notification.uuid,
                "dateTime": new_notification.dateTime.strftime("%Y-%m-%d %H:%M:%S"),
                "notificationLog": new_notification.notificationLog,
                "status": new_notification.status
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "code": 500,
            "message": "An error occurred while creating the consultation record.",
            "error": str(e)
        }), 500
    
@app.route("/notifications", methods=["GET"])
def get_notifications():
    notifications = notification.query.all()
    return jsonify([
        {
            "uuid": n.uuid,
            "dateTime": n.dateTime.strftime("%Y-%m-%d %H:%M:%S"),
            "notificationLog": n.notificationLog,
            "status": n.status
        }
        for n in notifications
    ]), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 