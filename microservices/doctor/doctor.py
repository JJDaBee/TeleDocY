import threading
import time
import os
import subprocess
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# PostgreSQL Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI', 'postgresql+psycopg2://postgres:postgres@localhost:5432/doctor')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)