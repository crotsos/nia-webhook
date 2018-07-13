from seq2seq import *

seq2seq.init()


def get_params(req):
    result = req.get("queryResult")
    id = result.get("intent").get("displayName")
    parameters = result.get("parameters")

    origin = parameters.get("origin")
    if isinstance(origin, dict):
        origin = next(iter(parameters.get("origin").values()), '').strip()

    destination = parameters.get("destination")
    if isinstance(destination, dict):
        destination = next(iter(parameters.get("destination").values()), '').strip()

    targets = parameters.get("target")
    middleboxes = parameters.get("middlebox")

    qos = None

    start = parameters.get("start")
    if isinstance(start, dict):
        start = next(iter(parameters.get("start").values()), '').strip()

    end = parameters.get("end")
    if isinstance(end, dict):
        end = next(iter(parameters.get("end").values()), '').strip()

    allow = parameters.get("allow")
    block = parameters.get("block")

    return id, origin, destination, targets, middleboxes, qos, start, end, allow, block


def build_nile_intent(req):
    id, origin, destination, targets, middleboxes, qos, start, end, allow, block = get_params(req)

    intent = seq2seq.translate(id, origin, destination, targets, middleboxes, qos, start, end, allow, block)
    for op in config.NILE_OPERATIONS:
        intent = intent.replace(op + " ", "  \n&nbsp;&nbsp;&nbsp;&nbsp;**" + op + "** ")

    speech = "Is this what you want?"
    print("Response:", speech + " " + intent)

    return {
        "fulfillmentText": speech,
        "fulfillmentMessages": [
            {
                "text": {
                    "text": speech + " " + intent
                }
            }
        ],
        "payload": {
            "google": {
                "expectUserResponse": True,
                "richResponse": {
                    "items": [
                        {
                            "simpleResponse": {
                                "textToSpeech": speech
                            }
                        },
                        {
                            "basicCard": {
                                "title": "Here is your intent.",
                                "formattedText": intent
                            }
                        }
                    ]
                }
            }
        },
        "outputContexts": [
            {
                "name": "projects/nira-68681/agent/sessions/eeeadd4f-8905-fed6-7919-b28ee616bd51/contexts/build-followup",
                "lifespanCount": 5,
                "parameters": {
                    "intent": intent
                }
            }
        ]
    }


def build_accepted(req):
    print("accepted", req)
    return {
        "payload": {
            "google": {
                "expectUserResponse": False,
                "richResponse": {
                    "items": [
                        {
                            "simpleResponse": {
                                "textToSpeech": "Okay! Intent compiled and deployed!"
                            }
                        }
                    ]
                }
            }
        }
    }


def build_feedback(req):
    print("denied", req)
    return {
        "payload": {
            "google": {
                "expectUserResponse": False,
                "richResponse": {
                    "items": [
                        {
                            "simpleResponse": {
                                "textToSpeech": "Okay! Intent compiled and deployed!"
                            }
                        }
                    ]
                }
            }
        }
    }


actions = {
    "build.nile": build_nile_intent,
    "build.build-yes": build_accepted,
    "build.build-no": build_feedback
}
