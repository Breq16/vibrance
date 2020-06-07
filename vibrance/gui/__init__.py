import sys
import threading

from flask import Flask, send_file, send_from_directory, request, jsonify, render_template

from .. import manager

app = Flask(__name__)

manager = manager.Manager()
manager.configure(sys.argv[1])

@app.route("/")
def index():
    return render_template("index.html", manager=manager)

@app.route("/static/index.css")
def staticfile():
    return send_file("templates/index.css")

@app.route("/static/index.js")
def staticjs():
    return send_file("templates/index.js")

@app.route("/input", methods=["POST"])
def input():
    data = request.json
    manager.chooseInput(manager.inputs[data["input"]])
    return ""

@app.route("/script", methods=["POST"])
def script():
    data = request.json
    manager.chooseScript(manager.scripts[data["script"]])
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
    appthread = threading.Thread(target=app.run)
    appthread.start()

    manager.run()
