from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

def track_msc_api(bl_number):
    url = "https://www.msc.com/api/feature/tools/TrackingInfo"
    headers = {
        "Content-Type": "application/json",
        "Referer": "https://www.msc.com/track-a-shipment",
        "Origin": "https://www.msc.com",
        "User-Agent": "Mozilla/5.0"
    }
    payload = {
        "SearchBy": "B",  # B for BL, C for Container
        "Numbers": [bl_number]
    }

    response = requests.post(url, json=payload, headers=headers)
    try:
        data = response.json()
        # 🔵 Burda Render loglarında görə bilmək üçün print edirik
        print("🔎 MSC raw result:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return data
    except Exception as e:
        return {
            "error": "JSON parse error",
            "details": str(e),
            "raw": response.text
        }

@app.route("/track", methods=["POST"])
def track():
    try:
        data = request.get_json()
        bl_number = data.get("bl_number", "").strip()

        if not bl_number:
            return jsonify({"error": "BL number is required"}), 400

        result = track_msc_api(bl_number)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500
