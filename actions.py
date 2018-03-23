import seq2seq

seq2seq.init()


def get_params(req):
    username = req.get("id")
    result = req.get("result")
    parameters = result.get("parameters")

    origin = parameters.get("origin")
    destination = parameters.get("destination")
    targets = parameters.get("target")
    middleboxes = parameters.get("middlebox")
    start = parameters.get("start")
    end = parameters.get("end")
    allow = parameters.get("allow")
    block = parameters.get("block")

    return username, origin, destination, targets, middleboxes, start, end, allow, block


def build_nip(req):
    print("args", middleboxes, targets)

    username, origin, destination, targets, middleboxes, start, end, allow, block = get_params(req)

    intent = seq2seq.translate(username, origin, destination, targets, middleboxes, start, end, allow, block)
    speech = "Is this what you want? " + nip
    print("Response:", speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "nia"
    }


actions = {
    "input.waypoint": build_waypoint_nip
}
