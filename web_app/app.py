#!/usr/bin/env python

from flask import Flask, render_template, request

import sys
sys.path.insert(0, './python-chess')
sys.path.insert(0, './core')

import chess
import nmodels

board = chess.Board()

nmodels.NModels.set_model(nmodels.ConvNetModel("models/my_model"))
nmodels.NModels.get_model().model.load_weights("models/model_1_2048.h5")


app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/start", methods=["GET"])
def start():
    board.reset()
    return nmodels.NModels.get_model().predict(board)


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/move", methods=["POST"])
def move():
    # print(request.form)
    fen = list(request.form.to_dict().keys())[0]
    board.set_fen(fen)
    return nmodels.NModels.get_model().predict(board)


if __name__ == "__main__":
    app.run(debug=True)
