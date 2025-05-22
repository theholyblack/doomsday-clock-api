from flask import Flask, jsonify
from countdoom.client import CountdoomClient

app = Flask(__name__)

@app.route("/")
def home():
    return "Doomsday Clock API (Powered by CountdoomClient)"

@app.route("/api/doomsday")
def get_doomsday():
    try:
        client = CountdoomClient()
        countdown = client.get_clock()
        return jsonify({
            "sentence": countdown.sentence,
            "seconds": countdown.seconds,
            "clock": countdown.clock,
            "time": countdown.time,
            "minutes": countdown.minutes
        })
    except Exception as e:
        return jsonify({"error": "Failed to get countdown", "details": str(e)}), 500
