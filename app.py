from __future__ import print_function

import json
import os

import requests

from actions import *
from flask import Flask, make_response, request
from future.standard_library import install_aliases

PROJECT_ID = "nira-68681"
PROJECT_API_BASE = "https://dialogflow.googleapis.com/v2/projects/" + PROJECT_ID + "/agent/"
HEADERS = {"Authorization": "Bearer $(gcloud auth application-default print-access-token)"}

install_aliases()

# Flask app should start in global layout
app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return "Network Intent Assistent (Nia) Webhook APIs"


@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json(silent=True, force=True)

    entity = {
        "name": "projects/" + PROJECT_ID + "/agent/entityTypes/example",
        "displayName": "example",
        "kind": 'KIND_MAP',
        "autoExpansionMode": "AUTO_EXPANSION_MODE_DEFAULT",
        "entities": [
            {
                {
                    "value": "example",
                    "synonyms": [
                        "examples", "ex.:", "e.g."
                    ]
                }
            }
        ]
    }
    r = requests.post(PROJECT_API_BASE + '/entityTypes', data=json.dumps(entity), headers=HEADERS)

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

    r = make_response(res)
    r.headers["Content-Type"] = "application/json"
    return r


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host="0.0.0.0")
