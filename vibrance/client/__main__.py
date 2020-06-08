from flask import Flask, send_file, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/selector.html")
def selector():
    return render_template("selector.html", host="cloud.itsw.es")

@app.route("/app.html")
def apphtml():
    return render_template("app.html")

@app.route("/app.js")
def appjs():
    return send_file("templates/app.js")

@app.route("/viewall.html")
def viewall():
    return render_template("viewall.html", host="cloud.itsw.es")

@app.route("/stress.html")
def stress():
    return render_template("stress.html", host="cloud.itsw.es")

if __name__ == "__main__":
    app.run("0.0.0.0", port=8080)
