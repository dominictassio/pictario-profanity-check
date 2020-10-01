from profanity_check import predict_prob
from flask import Flask, abort, make_response, request


app = Flask("pictario-profanity-check")


@app.route("/", methods=["POST"])
def check():
    if request.method != "POST":
        abort(404)

    if not validate_token(request.form["token"]):
        abort(404)

    return predict_prob([str(request.form["message"])])


def validate_token(token):
    return token == "00000000"
