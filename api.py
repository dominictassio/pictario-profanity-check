import os
from profanity_filter import ProfanityFilter
from flask import Flask, abort, make_response, request
from flask_httpauth import HTTPTokenAuth
from functools import lru_cache


app = Flask("pictario-profanity-check")
auth = HTTPTokenAuth(scheme="Bearer")
AUTH_TOKEN = os.environ["TOKEN"]
CACHE_SIZE = os.environ.get("CACHE_SIZE", 128)
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
def endpoint_handle():
    if request.content_type != "text/plain":
        abort(400)

    text = request.get_data(as_text=True)

    if "censor" in request.path:
        result = censor(text)

    if "is-profane" in request.path:
        result = str(pfilter.is_profane(text)).lower()

    response = make_response(result)
    response.mimetype = "text/plain"

    return response


@lru_cache(maxsize=CACHE_SIZE)
def censor(text):
    return pfilter.censor(text)
