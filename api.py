import os
from profanity_filter import ProfanityFilter
from flask import Flask, abort, make_response, request
from flask_httpauth import HTTPTokenAuth


app = Flask("pictario-profanity-check")
auth = HTTPTokenAuth(scheme="Bearer")
AUTH_TOKEN = os.environ["TOKEN"]
pfilter = ProfanityFilter(languages=["en_core_web_sm"])


@auth.verify_token
def verify_token(token):
    return AUTH_TOKEN is not None and token == AUTH_TOKEN


@app.route("/")
def index():
    return {"api_version": "v1"}


@app.route("/v1/censor/", methods=["POST"])
@app.route("/v1/is-profane/", methods=["POST"])
@auth.login_required
def censor():
    if request.content_type != "text/plain":
        abort(400)

    data = request.get_data(as_text=True)

    if "censor" in request.path:
        result = pfilter.censor(data)

    if "is-profane" in request.path:
        result = pfilter.is_profane(data)

    response = make_response(str(result))
    response.mimetype = "text/plain"

    return response
