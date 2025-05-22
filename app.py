from flask import Flask, jsonify
import subprocess
import json

app = Flask(__name__)

@app.route("/")
def home():
    return "Doomsday Clock API (Powered by Countdoom CLI)"

@app.route("/api/doomsday")
def get_doomsday():
    try:
        # Run the countdoom CLI with JSON output
        result = subprocess.run(['countdoom', '--format', 'json'], capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        return jsonify(data)
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Failed to get countdown", "details": e.stderr}), 500
    except Exception as e:
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500
