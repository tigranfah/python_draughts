#!/usr/bin/env python

from flask import Flask, render_template, request
import nmodels

import sys
sys.path.insert(0, '.')
# import nmodels


app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/start", methods=["GET"])
def start():
    return "e2e4"


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/move", methods=["POST"])
def move():
    return "g1f3"


if __name__ == "__main__":
    app.run(debug=True)
