from flask import Flask, request, jsonify
from trackers import msc_api

app = Flask(__name__)

@app.route("/debug", methods=["POST"])
def debug():
    data = request.get_json()
    print("📦 Received:", data)
    return jsonify({"received": data, "success": True})

@app.route("/track", methods=["POST"])
def track():
    data = request.get_json()
    bl_number = data.get("bl_number", "").strip()

    print("🔍 Tracking BL:", bl_number)

    if not bl_number:
        return jsonify({"success": False, "error": "Missing BL number"}), 400

    result = msc_api.track_msc(bl_number)
    return jsonify(result)
