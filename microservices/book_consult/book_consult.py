from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import pika
import sys, os
from os import environ

import amqp_lib
from invokes import invoke_http

app = Flask(__name__)

CORS(app)