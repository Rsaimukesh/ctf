from flask import Flask, render_template, redirect, send_from_directory

app = Flask(__name__)

@app.route("/robots.txt")
def robots():
    return send_from_directory(app.static_folder, "robots.txt")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/when")
def when():
    return render_template("when.html")

@app.route("/what")
def what():
    return render_template("what.html")

@app.route("/who")
def who():
    return render_template("who.html")

@app.route("/why")
def why():
    return render_template("why.html")

if __name__ == "__main__":
    app.run(debug=False)


