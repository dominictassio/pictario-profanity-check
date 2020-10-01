import os
from profanity_check import predict_prob
from flask import Flask, abort, jsonify, request
from flask_httpauth import HTTPTokenAuth


app = Flask("pictario-profanity-check")
auth = HTTPTokenAuth(scheme="Bearer")
AUTH_TOKEN = os.environ["TOKEN"]


@auth.verify_token
def verify_token(token):
    return AUTH_TOKEN is not None and token == AUTH_TOKEN


@app.route("/")
def index():
    return "<p>v1</p>"


@app.route("/v1/", methods=["POST"])
@auth.login_required
def check():
    if not request.is_json:
        abort(400)

    json = request.get_json()

    if type(json) is not list or any(type(message) is not str for message in json):
        abort(422)

    return jsonify(predict_prob(json).tolist())
