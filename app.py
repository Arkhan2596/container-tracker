from flask import Flask, request, jsonify
import asyncio
import nest_asyncio
from trackers import msc_scrape  # <- Async funksiya

# Nest asyncio: Gunicorn ilə async loop problemi olmur
nest_asyncio.apply()

app = Flask(__name__)

@app.route('/')
def index():
    return 'MSC Container Tracking API (Scraping-based) is running.'

@app.route('/track', methods=['POST'])
def track():
    try:
        data = request.json
        bl_number = data.get('bl_number', '').strip()
        container_number = data.get('container_number', '').strip()
        shipping_line = data.get('shipping_line', '').lower().strip()

        print("📦 Received data:", data)

        result = {
            "etd_pol": "No result found",
            "eta_transshipment": "No result found",
            "etd_transshipment": "No result found",
            "feeder": "No result found",
            "eta_pod": "No result found",
            "raw_result": {}
        }

        if shipping_line == "msc":
            # async funksiyanı sync kontekstdə işlət
            loop = asyncio.get_event_loop()
            msc_result = loop.run_until_complete(msc_scrape.track_msc(bl_number))
            print("🔧 MSC scrape result:", msc_result)
            result["raw_result"] = msc_result

        return jsonify(result)

    except Exception as e:
        print("🔥 General error:", str(e))
        return jsonify({"error": str(e)})
