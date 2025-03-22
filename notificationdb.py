#just to store notification logs w/ status

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/notificationdb' #rmb to change name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)
def run_sql_file(filename):
    """ Runs an SQL file to create the table and insert initial data """
    with open(filename, 'r') as file:
        sql_script = file.read()

    # Establish a connection and run the script
    connection = db.engine.raw_connection()  # Using SQLAlchemy engine to get a connection

    try:
        cursor = connection.cursor()
        for statement in sql_script.split(';'):
            if statement.strip():  # Skip empty statements
                cursor.execute(statement)
        connection.commit()
        print("SQL script executed successfully!")
    except Exception as e:
        print(f"Error executing SQL script: {e}")
    finally:
        connection.close()

def table_exists():
    """Check if the table exists in the database"""
    try:
        # Check if consultationHistory table exists by querying it
        result = db.session.execute('SHOW TABLES LIKE "consultationHistory"')
        return result.fetchone() is not None
    except OperationalError as e:
        # If an error occurs while querying, treat it as the table not existing
        print(f"Error checking table existence: {e}")
        return False

# Run the SQL file when the app starts, but only if the table does not exist yet
if not table_exists():
    run_sql_file('notificationdb.sql')

class notification(db.Model):
    __tablename__ = "notificaiton"

    patientId=db.Column(db.Integer, primary_key = True)
    NRIC=db.Column(db.String(9), autoincrement=False)
    notificationLog=db.Column(db.String(1000),nullable=False)
    dateTime=db.Column(db.DateTime,nullable=False)
    status=db.Column(db.String(100),nullable=False)


@app.route("/notificationdb", methods=["POST"]) #rmb to change name (not sure if clash)
def create_notificationrecord():
    data = request.get_json()
    patientId=data.get("patientId")
    NRIC = data.get("NRIC")
    dateTime = data.get("dateTime")
    notificationLog=data.get("notificationLog")
    status=data.get("status")

    new_notification = notification(
        patientId=patientId,
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
                "patientId" : new_notification.patientId,
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
    app.run(port=5000, debug=True) # have not changed port num