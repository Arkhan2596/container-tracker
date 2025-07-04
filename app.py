from flask import Flask, request, jsonify
from trackers import msc
from utils.cleanup import clean_input

app = Flask(__name__)

@app.route("/track", methods=["POST"])
def track():
    data = request.get_json()
    container_number = data.get("container_number", "")
    bl_number = data.get("bl_number", "")
    shipping_line = data.get("shipping_line", "").lower()

    if shipping_line == "msc":
        result = msc.track(container_number, bl_number)
        return jsonify({
            "raw_result": result,  # bunu əlavə etdik
            "etd_pol": result.get("etd_from_pol", ""),
            "eta_transit": result.get("eta_transshipment", ""),
            "etd_transit": result.get("etd_transshipment", ""),
            "feeder": result.get("feeder_name", ""),
            "eta_pod": result.get("eta_pod", "")
        })

    return jsonify({"error": "Unsupported shipping line."})
