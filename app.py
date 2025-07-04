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

        result = {
            "etd_pol": "No result found",
            "eta_transshipment": "No result found",
            "etd_transshipment": "No result found",
            "feeder": "No result found",
            "eta_pod": "No result found",
            "raw_result": {}
        }

        if shipping_line == "msc":
            msc_result = msc_scrape.track_msc(container_number, bl_number)  # Scraper funksiyası
            print("MSC result:", msc_result)

            for key in result:
                if key in msc_result and msc_result[key]:
                    result[key] = msc_result[key]

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
