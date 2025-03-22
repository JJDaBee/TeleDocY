from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/medicineInventory'
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
    run_sql_file('medicineInventory.sql')

class medicineInventory(db.Model):
    __tablename__ = "medicineInventory"

    medicationID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    medication = db.Column(db.String(255), nullable=False)  
    price = db.Column(db.DECIMAL(10, 2), nullable=False) 
    quantityLeft = db.Column(db.Integer, nullable=False, default=0)  
    nextRestockDate = db.Column(db.DateTime, default=None) 
    allergies = db.Column(db.String(1000), default="None")


@app.route("/medicineInventory/<string:medicationID>") 
def find_by_medicationID(medicationID):
    # quantity = request.args.get("qty", default=1, type=int)
    available_meds = medicineInventory.query.filter_by(medicationID=medicationID).first()


    if available_meds:
        return jsonify(
        {
            "code": 200,
            "data": {
                "medicationID": available_meds.medicationID,
                "medication": available_meds.medication,
                "price": float(available_meds.price),
                "quantityLeft": available_meds.quantityLeft,
                "isAvailable": available_meds.quantityLeft > 0,
                # "sufficientStock": (available_meds.quantityLeft >= quantity) if quantity is not None else None
            }
        }
    ), 200
    return jsonify(
        {
            "code": 404,
            "message": "medicine not available."
        }
    ), 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)