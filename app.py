from flask import Flask, jsonify
from countdoom import Countdown

app = Flask(__name__)

@app.route("/")
def home():
    return "Doomsday Clock API (Powered by Countdoom)"

@app.route("/api/doomsday")
def get_doomsday():
    try:
        countdown = Countdown()
        return jsonify({
            "sentence": countdown.sentence,
            "seconds": countdown.seconds,
            "clock": countdown.clock,
            "time": countdown.time,
            "minutes": countdown.minutes,
        })
    except Exception as e:
        return jsonify({"error": "Failed to get countdown", "details": str(e)}), 500
