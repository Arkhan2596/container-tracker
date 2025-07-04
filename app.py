from flask import Flask, request, jsonify
from trackers import msc_scrape  # <- Yeni scraping faylı

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

        print("📦 Received data:", data)  # Əlavə et

        result = {
            "etd_pol": "No result found",
            "eta_transshipment": "No result found",
            "etd_transshipment": "No result found",
            "feeder": "No result found",
            "eta_pod": "No result found",
            "raw_result": {}
        }

        if shipping_line == "msc":
            from trackers import msc_scrape
            msc_result = msc_scrape.track_msc(bl_number)

            print("🔧 MSC scrape result:", msc_result)  # Əlavə et

            result["raw_result"] = msc_result

        return jsonify(result)

    except Exception as e:
        print("🔥 General error:", str(e))  # Əlavə et
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
