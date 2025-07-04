from flask import Flask, request, jsonify
import asyncio
import nest_asyncio
from trackers import track_msc  # bu dəyişdi

nest_asyncio.apply()
app = Flask(__name__)

@app.route('/')
def index():
    return 'MSC Container Tracking API is running.'

@app.route('/track', methods=['POST'])
def track():
    try:
        data = request.json
        bl_number = data.get('bl_number', '').strip()
        shipping_line = data.get('shipping_line', '').lower().strip()

        print("📦 Received data:", data)

        result = {
            "etd_pol": "Yoxdur",
            "eta_transshipment": "Yoxdur",
            "etd_transshipment": "Yoxdur",
            "feeder": "Yoxdur",
            "eta_pod": "Yoxdur"
        }

        if shipping_line == "msc":
            loop = asyncio.get_event_loop()
            msc_data = loop.run_until_complete(track_msc(bl_number))
            if msc_data.get("success"):
                result.update(msc_data)
            else:
                return jsonify({"error": msc_data.get("error", "Unknown error")})

        return jsonify(result)

    except Exception as e:
        print("🔥 General error:", str(e))
        return jsonify({"error": str(e)})
