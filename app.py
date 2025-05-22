from flask import Flask, jsonify
import subprocess
import json
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

@app.route("/")
def home():
    return "Midnight Array API: /api/status for combined data"

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

# --- Helpers ---

def get_doomsday_data():
    try:
        result = subprocess.run(['countdoom', '--format', 'json'], capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except Exception as e:
        return {"error": "Failed to get doomsday clock", "details": str(e)}

def get_defcon_data():
    try:
        url = "https://www.defconlevel.com/"
        headers = { "User-Agent": "Mozilla/5.0" }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(separator=" ", strip=True)
        return extract_defcon_from_text(text)
    except Exception as e:
        return None  # or return a default value like 5

def extract_defcon_from_text(text):
    match = re.search(r"DEFCON\s*([1-5])", text.upper())
    if match:
        return int(match.group(1))
    return None
