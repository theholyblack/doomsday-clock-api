from flask import Flask, jsonify
import subprocess
import json
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

@app.route("/")
def home():
    return "Midnight Array API: Visit /api/status for combined data"

@app.route("/api/status")
def get_combined_status():
    return jsonify({
        "doomsday": get_doomsday_data(),
        "defcon": get_defcon_data()
    })

@app.route("/api/doomsday")
def api_doomsday():
    return jsonify(get_doomsday_data())

@app.route("/api/defcon")
def api_defcon():
    return jsonify({"defcon": get_defcon_data()})

# --- Helper Functions ---

def get_doomsday_data():
    try:
        result = subprocess.run(['countdoom', '--format', 'json'], capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except Exception as e:
        return {"error": "Failed to get Doomsday Clock data", "details": str(e)}

def get_defcon_data(
