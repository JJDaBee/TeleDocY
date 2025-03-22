from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/consultationHistory'
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
    run_sql_file('consultationHistory.sql')

class consultationHistory(db.Model):
    __tablename__ = "consultationHistory"

    patientId=db.Column(db.Integer, primary_key=True)
    NRIC=db.Column(db.String(9), autoincrement=False)
    dateTime=db.Column(db.DateTime,primary_key=True)
    reasonForVisit=db.Column(db.String(1000), nullable=False)
    doctorName= db.Column(db.String(100), nullable=False)
    diagnosis=db.Column(db.String(1000), nullable=False)
    prescriptions=db.Column(db.String(1000), default=None)


@app.route("/consultationHistory/<int:patientId>")
def find_by_patientId(patientId):
    # quantity = request.args.get("qty", default=1, type=int)
    indiv_history = consultationHistory.query.filter_by(patientId=patientId).all()

    if not indiv_history:
        return jsonify(
            {
                "code": 404,
                "message": "No consultation history found for this patientId."
            }
        ), 404
    
    indiv_historylist = []
    for record in indiv_history:
        indiv_historylist.append({
            "NRIC": record.NRIC,
            "dateTime": record.dateTime.strftime("%Y-%m-%d %H:%M:%S"),
            "reasonForVisit": record.reasonForVisit,
            "doctorName": record.doctorName,
            "diagnosis": record.diagnosis,
            "prescriptions": record.prescriptions
    })
    
    return jsonify(
        {
            "code":200,
            "data": indiv_historylist
        }
    ), 200

@app.route("/consultationHistory", methods=["POST"])
def create_consultationrecord():
    data = request.get_json()
    patientId= data.get("patientId")
    NRIC = data.get("NRIC")
    dateTime = data.get("dateTime")
    reasonForVisit = data.get("reasonForVisit")
    doctorName = data.get("doctorName")
    diagnosis = data.get("diagnosis")
    prescriptions = data.get("prescriptions")

    new_consultation = consultationHistory(
        patientId=patientId,
        NRIC=NRIC,
        dateTime=dateTime,
        reasonForVisit=reasonForVisit,
        doctorName=doctorName,
        diagnosis=diagnosis,
        prescriptions=prescriptions
    )
    try:
        # Add the new consultation to the session and commit to the database
        db.session.add(new_consultation)
        db.session.commit()

        return jsonify({
            "code": 201,
            "message": "Consultation record created successfully.",
            "data": {
                "patientId": new_consultation.patientId,
                "NRIC": new_consultation.NRIC,
                "dateTime": new_consultation.dateTime.strftime("%Y-%m-%d %H:%M:%S"),
                "reasonforVisit": new_consultation.reasonForVisit,
                "doctorName": new_consultation.doctorName,
                "diagnosis": new_consultation.diagnosis,
                "prescriptions": new_consultation.prescriptions
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