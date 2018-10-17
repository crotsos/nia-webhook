""" Network Wizard Webhook actions """

import parser

import beautifier
import interpreter


def build_nile_intent(request):
    """ Webhook action to build Nile intent from Dialogflow request """
    entities = parser.parse_intent(request)

    intent = interpreter.translate(entities)
    beautified_intent = beautifier.beautify(intent)

    speech = "Is this what you want?"
    print("Response:", speech + " " + intent)

    return {
        "fulfillmentText": speech,
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [speech + " " + intent]
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
                                "formattedText": beautified_intent
                            }
                        }
                    ]
                }
            }
        },
        "outputContexts": [
            {
                "name": "projects/nira-68681/agent/sessions/eeeadd4f-8905-fed6-7919-b28ee616bd51/contexts/build-followup",
                "lifespanCount": 10,
                "parameters": {
                    "intent": intent,
                    "inputText": request.get("queryResult").get("queryText")
                }
            }
        ]
    }


def build_accepted(request):
    """ Webhook action to deploy Nile intent after user confirmation """

    print("accepted", request)
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


def build_feedback(request):
    """ Webhook action to receive feedback from user after rejecting built intent """

    print("feedback", request)
    original_intent, entity, value = parser.parse_feedback(request)
    print("feedback", original_intent, entity, value)
    return {
        "payload": {
            "google": {
                "expectUserResponse": False,
                "richResponse": {
                    "items": [
                        {
                            "simpleResponse": {
                                "textToSpeech": "Hmm, can you tell me what information I missed then?"
                            }
                        }
                    ]
                }
            }
        }
    }


ACTIONS = {
    "build.nile": build_nile_intent,
    "build.build-yes": build_accepted,
    "build.build-no.feedback": build_feedback
}
