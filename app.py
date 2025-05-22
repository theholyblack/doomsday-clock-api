from flask import Flask, jsonify
import subprocess
import json
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

@app.route("/")
def home():
    return "Midnight Array API (Doomsday + DEFCON)"

@app.route("/api/status")
def get_combined_status():
    try:
        # === DOOMSDAY CLOCK ===
        doomsday_data = {}
        result = subprocess.run(['countdoom', '--format', 'json'], capture_output=True, text=True, check=True)
        doomsday_data = json.loads(result.stdout)

        # === DEFCON LEVEL ===
        url = "https://www.defconlevel.com/"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        level_text = soup.find("h2", string=lambda t: t and "defcon" in t.lower())
        if not level_text:
            para = soup.find("p", string=lambda t: t and "defcon" in t.lower())
            if para:
                defcon = extract_defcon_from_text(para.text)
            else:
                defcon = None
        else:
            defcon = extract_defcon_from_text(level_text.text)

        return jsonify({
            "doomsday": doomsday_data,
            "defcon": defcon
        })

    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Failed to get countdown", "details": e.stderr}), 500
    except Exception as e:
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500

@app.route("/api/doomsday")
def get_doomsday():
    try:
        result = subprocess.run(['countdoom', '--format', 'json'], capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        return jsonify(data)
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Failed to get countdown", "details": e.stderr}), 500
    except Exception as e:
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500

@app.route("/api/defcon")
def get_defcon_level():
    try:
        url = "https://www.defconlevel.com/"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        level_text = soup.find("h2", string=lambda t: t and "defcon" in t.lower())
        if not level_text:
            para = soup.find("p", string=lambda t: t and "defcon" in t.lower())
            if para:
                level = extract_defcon_from_text(para.text)
            else:
                return jsonify({"error": "Could not find DEFCON text"}), 500
        else:
            level = extract_defcon_from_text(level_text.text)

        return jsonify({"defcon": level})
    except Exception as e:
        return jsonify({"error": "Failed to scrape DEFCON level", "details": str(e)}), 500

def extract_defcon_from_text(text):
    match = re.search(r"DEFCON\s*([1-5])", text.upper())
    if match:
        return int(match.group(1))
    return None

