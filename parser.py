""" Entities parser """


def to_camel_case(string):
    """ Converts string to camel case """
    output = ''.join(x for x in string.title() if x.isalnum())
    return output[0].lower() + output[1:]


def parse_intent(request):
    """ Parses extracted entities from Dialogflow build_intent request """

    result = request["queryResult"]
    entities = {}
    entities["id"] = result["intent"]["displayName"]

    parameters = result["parameters"]

    if "origin" in parameters and parameters["origin"]:
        entities["origin"] = parameters["origin"]
        if isinstance(entities["origin"], dict):
            entities["origin"] = next(iter(parameters["origin"].values()), "").strip()

    if "destination" in parameters and parameters["destination"]:
        entities["destination"] = parameters["destination"]
        if isinstance(entities["destination"], dict):
            entities["destination"] = next(iter(parameters["destination"].values()), "").strip()

    if "target" in parameters and parameters["target"]:
        entities["targets"] = parameters["target"]

    if "middlebox" in parameters and parameters["middlebox"]:
        entities["middleboxes"] = parameters["middlebox"]

    if "qos_metric" in parameters and parameters["qos_metric"] and "qos_value" in parameters and parameters["qos_value"]:
        metric = {}
        metric["name"] = to_camel_case(parameters["qos_metric"])
        metric["value"] = parameters["qos_value"] if isinstance(parameters["qos_value"], basestring) else parameters["qos_value"]["number-integer"]
        if "qos_constraint" in parameters and parameters["qos_constraint"]:
            metric["constraint"] = parameters["qos_constraint"]
        if "qos_unit" in parameters and parameters["qos_unit"]:
            metric["unit"] = parameters["qos_unit"]

        entities["qos"] = [metric]

    if "start" in parameters and parameters["start"]:
        entities["start"] = parameters["start"]
        if isinstance(entities["start"], dict):
            entities["start"] = next(iter(parameters["start"].values()), "").strip()

    if "end" in parameters and parameters["end"]:
        entities["end"] = parameters["end"]
        if isinstance(entities["end"], dict):
            entities["end"] = next(iter(parameters["end"].values()), "").strip()

    return entities


def parse_feedback(request):
    """ Parses entities from Dialogflow user_feedback request to train agent """

    result = request["queryResult"]
    parameters = result["parameters"]

    feedback = {}
    feedback["original_intent"] = ""
    feedback["entity"] = parameters["entity"]
    feedback["value"] = parameters["value"]

    return feedback
