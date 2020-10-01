import os
from profanity_filter import ProfanityFilter
from flask import Flask, abort, make_response, request
from flask_httpauth import HTTPTokenAuth


app = Flask("pictario-profanity-check")
auth = HTTPTokenAuth(scheme="Bearer")
AUTH_TOKEN = os.environ["TOKEN"]
pfilter = ProfanityFilter()


@auth.verify_token
def verify_token(token):
    return AUTH_TOKEN is not None and token == AUTH_TOKEN


@app.route("/")
def index():
    return {
        "api_version": "v1"
    }


@app.route("/v1/censor/", methods=["POST"])
@auth.login_required
def censor():
    return handle_method(pfilter.censor)


@app.route("/v1/is-profane/", methods=["POST"])
@auth.login_required
def is_profane():
    return handle_method(pfilter.is_profane)


def handle_method(method):
    if request.content_type != "text/plain":
        abort(400)
    
    data = request.get_data(as_text=True)
    result = method(data)
    response = make_response(str(result))
    response.mimetype = "text/plain"

    return response
