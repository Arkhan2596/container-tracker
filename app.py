from flask import Flask, request, jsonify
from trackers import msc
from utils.cleanup import clean_input

app = Flask(__name__)

@app.route("/track", methods=["POST"])
def track():
    data = request.json
    container_number = clean_input(data.get("container_number", ""))
    bl_number = clean_input(data.get("bl_number", ""))
    shipping_line = clean_input(data.get("shipping_line", "")).lower()

    result = {
        "etd_pol": "",
        "eta_transit": "",
        "etd_transit": "",
        "feeder": "",
        "eta_pod": "",
        "status": "No result found"
    }

    try:
        if shipping_line == "msc":
            result = msc.track_msc(container_number, bl_number)
            print("MSC nəticəsi:", result)      

    except Exception as e:
        result["status"] = f"Error: {str(e)}"

    return jsonify(result)
