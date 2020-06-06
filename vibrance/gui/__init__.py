from flask import Flask, send_file, send_from_directory, request, jsonify

from . import manager

app = Flask(__name__)

manager = manager.Manager()

@app.route("/")
def index():
    return send_file("static/index.html")

@app.route("/static/<path:path>")
def static(path):
    return send_from_directory("css", path)

@app.route("/input", methods=["POST"])
def input():
    return ""

@app.route("/script", methods=["POST"])
def script():
    return ""

@app.route("/relay", methods=["POST"])
def relay():
    data = request.json
    manager.connect(data["host"], (data["psk"] if "psk" in data else None))
    return ""

@app.route("/status")
def status():
    return jsonify(manager.getStatus())

if __name__ == "__main__":
    app.run()
