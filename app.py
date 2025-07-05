from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/debug", methods=["POST"])
def debug():
    data = request.json
    print("DEBUG DATA RECEIVED:", data)
    return jsonify({"success": True, "received": data})
