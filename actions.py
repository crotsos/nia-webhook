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
    print("Response:", speech)

    return {
        "speech": speech,
        "displayText": speech + intent,
        "data": intent,
        # "contextOut": [],
        "source": "nia"
    }


actions = {
    "input.nile": build_nile_intent
}
