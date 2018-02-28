# !/usr/bin/env python
# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function

import json
import os

from flask import Flask, make_response, request
from future.standard_library import install_aliases

install_aliases()

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return "Network Intent Assistent Webhook APIs"


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request: {}".format(json.dumps(req, indent=4)))
    res = build_nip(req)
    print("Response: {}".format(json.dumps(res, indent=4)))

    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def build_nip(req):
    result = req.get("result")
    parameters = result.get("parameters")

    middleboxes = parameters.get('middlebox')
    target = parameters.get('policy-target')
    console.log('args', middleboxes, target)
    nip = 'define intent customIntent:' + '\n   add ' + map(lambda mb: mb + ', ', middleboxes) + '\n   for ' + map(lambda pt: pt + ', ', target)

    speech = 'The info you gave me generated this program:\n ' + nip + '\n Is this what you want?'

    print("Response:", speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "nia"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
