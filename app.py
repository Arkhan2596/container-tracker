from flask import Flask, request, jsonify
from trackers import msc 

app = Flask(__name__)

@app.route('/')
def index():
    return 'MSC Container Tracking API is running.'

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
            msc_result = msc.track(container_number, bl_number)
            if msc_result.get("success"):
                result.update({
                    "etd_pol": msc_result.get("etd_pol", "No result found"),
                    "eta_transshipment": msc_result.get("eta_transshipment", "No result found"),
                    "etd_transshipment": msc_result.get("etd_transshipment", "No result found"),
                    "feeder": msc_result.get("feeder", "No result found"),
                    "eta_pod": msc_result.get("eta_pod", "No result found"),
                })
            result["raw_result"] = msc_result

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
