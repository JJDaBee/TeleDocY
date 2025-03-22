#just to store notification logs w/ status

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/notificationdb' #rmb to change name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

class notification(db.Model):
    __tablename__ = "notificaiton"

    NRIC=db.Column(db.String(9), primary_key=True, autoincrement=False)
    notificationLog=db.Column(db.String(1000),nullable=False)
    dateTime=db.Column(db.DateTime,nullable=False)
    status=db.Column(db.String(100),nullable=False)


@app.route("/notificationdb", methods=["POST"]) #rmb to change name (not sure if clash)
def create_notificationrecord():
    data = request.get_json()
    NRIC = data.get("NRIC")
    dateTime = data.get("dateTime")
    notificationLog=data.get("notificationLog")
    status=data.get("status")

    new_notification = notification(
        NRIC=NRIC,
        dateTime=dateTime,
        notificationLog=notificationLog,
        status=status 
    )
    try:
        # Add the new consultation to the session and commit to the database
        db.session.add(new_notification)
        db.session.commit()

        return jsonify({
            "code": 201,
            "message": "Notification record created successfully.",
            "data": {
                "NRIC": new_notification.NRIC,
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

if __name__ == '__main__':
    app.run(port=5000, debug=True)