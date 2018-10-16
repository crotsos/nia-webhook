from __future__ import print_function

import json
import os

import api
from actions import actions
from flask import Flask, make_response, request
from future.standard_library import install_aliases

install_aliases()

# Flask app should start in global layout
app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return "Network Intent Assistent (Nia) Webhook APIs"


@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request: {}".format(json.dumps(req, indent=4)))
    try:
        res = actions[req.get("queryResult").get("action")](req)
    except Exception as err:
        res = {
            "message": "Action not mapped in webhook.",
            "error": str(err)
        }
    res = json.dumps(res, indent=4)
    print("Response: {}".format(json.dumps(res, indent=4)))

    response = make_response(res)
    response.headers["Content-Type"] = "application/json"
    return response


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host="0.0.0.0")
