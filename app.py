from flask import Flask, request, jsonify
import asyncio
import nest_asyncio
from trackers import msc_scrape

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
            "etd_pol": "No result found",
            "eta_transshipment": "No result found",
            "etd_transshipment": "No result found",
            "feeder": "No result found",
            "eta_pod": "No result found"
        }

        if shipping_line == "msc":
            loop = asyncio.get_event_loop()
            msc_data = loop.run_until_complete(msc_scrape.track_msc(bl_number))
            if msc_data.get("success"):
                result.update({
                    "etd_pol": msc_data.get("etd_pol", ""),
                    "eta_transshipment": msc_data.get("eta_transshipment", ""),
                    "etd_transshipment": msc_data.get("etd_transshipment", ""),
                    "feeder": msc_data.get("feeder", ""),
                    "eta_pod": msc_data.get("eta_pod", "")
                })
            else:
                return jsonify({"error": msc_data.get("error", "Unknown error")})

        return jsonify(result)

    except Exception as e:
        print("🔥 General error:", str(e))
        return jsonify({"error": str(e)})
