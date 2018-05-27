from seq2seq import *

seq2seq.init()


def get_params(req):
    id = req.get("id")
    result = req.get("result")
    parameters = result.get("parameters")

    origin = parameters.get("origin")
    destination = parameters.get("destination")
    targets = parameters.get("target")
    middleboxes = parameters.get("middlebox")
    qos = None
    start = parameters.get("start")
    end = parameters.get("end")
    allow = parameters.get("allow")
    block = parameters.get("block")

    return id, origin, destination, targets, middleboxes, qos, start, end, allow, block


def build_nile_intent(req):
    id, origin, destination, targets, middleboxes, qos, start, end, allow, block = get_params(req)

    intent = seq2seq.translate(id, origin, destination, targets, middleboxes, qos, start, end, allow, block)
    speech = "Is this what you want? "
    print("Response:", speech)

    return {
        "speech": speech,
        "displayText": speech + intent,
        # "data": data,
        # "contextOut": [],
        "source": "nia"
    }


actions = {
    "input.nile": build_nile_intent
}
