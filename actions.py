from seq2seq import *

seq2seq.init()


def get_params(req):
    id = req.get("responseId")
    result = req.get("queryResult")
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
    speech = "Is this what you want? "
    print("Response:", speech + intent)

    return {
        "fulfillmentText": speech,
        "fulfillmentMessages": [
            {
                "card": {
                    "title": speech,
                    "subtitle": intent,
                    "imageUri": "https://assistant.google.com/static/images/molecule/Molecule-Formation-stop.png",
                    "buttons": [
                        {
                            "text": "Yes! :)",
                            "postback": "https://assistant.google.com/"
                        },
                        {
                            "text": "No! :(",
                            "postback": "https://assistant.google.com/"
                        }
                    ]
                }
            }
        ],
        "source": "nia-proxy.herokuapp.com",
        "payload": {
            "google": {
                "expectUserResponse": True,
                "richResponse": {
                    "items": [
                        {
                            "simpleResponse": {
                                "textToSpeech": speech
                            }
                        }
                    ]
                }
            }
        },
        "outputContexts": [
            {
                "name": "projects/${PROJECT_ID}/agent/sessions/${SESSION_ID}/contexts/context name",
                "lifespanCount": 5,
                "parameters": {
                    "intent": intent
                }
            }
        ],
        "followupEventInput": {
            "name": "cofirmation",
            "languageCode": "en-US",
            "parameters": {
                "intent": intent
            }
        }
    }


actions = {
    "input.nile": build_nile_intent
}
