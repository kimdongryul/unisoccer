from flask import jsonify, request, render_template
from app import app


@app.route('/')
def index():
    return render_template('test.html')


@app.route('/add/test', methods=["GET", "POST"])
def add_test():
    data = {}
    data["success"] = False
    if request.method == "POST":
        req = request.form
        data["result"] = int(req["number1"]) + int(req["number2"])
        data["success"] = True
        return jsonify(data)
    data["error"] = "Not GET methods, POST methods plz"
    return jsonify(data)
