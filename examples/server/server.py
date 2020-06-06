from flask import Flask, send_file, send_from_directory, request, jsonify

import vibrance

app = Flask(__name__)

ctrl = vibrance.Controller()

@app.route("/")
def index():
    return send_file("index.html")

@app.route("/css/<path:path>")
def css(path):
    return send_from_directory("css", path)

@app.route("/js/<path:path>")
def js(path):
    return send_from_directory("js", path)

@app.route("/input", methods=["POST"])
def input():
    return ""

@app.route("/script", methods=["POST"])
def script():
    return ""

@app.route("/relay", methods=["POST"])
def relay():
    data = request.json
    if ctrl.enabled:
        ctrl.close()
    ctrl.connect(data["host"], (data["psk"] if "psk" in data else None))
    return ""

@app.route("/status")
def status():
    info = {"input":{}, "script":{}, "relay":{}}

    if not ctrl.enabled:
        info["relay"]["enabled"] = False
    else:
        ctrl.socket.repair()
        info["relay"]["enabled"] = True
        if not ctrl.socket.connected:
            info["relay"]["connected"] = False
        else:
            info["relay"]["connected"] = True

    return jsonify(info)

if __name__ == "__main__":
    app.run()
