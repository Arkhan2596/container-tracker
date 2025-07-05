from flask import Flask, request, jsonify
import asyncio
from trackers import msc_api  # sənin faylın adlandırması belədirsə

app = Flask(__name__)

@app.route("/debug", methods=["POST"])
def debug():
    data = request.json
    print("DEBUG DATA RECEIVED:", data)
    return jsonify({"success": True, "received": data})

@app.route("/track", methods=["POST"])
def track():
    data = request.json
    bl_number = data.get("bl_number", "")
    if not bl_number:
        return jsonify({"success": False, "error": "bl_number missing"}), 400

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    msc_data = loop.run_until_complete(msc_api.track_msc(bl_number))
    loop.close()

    return jsonify(msc_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
