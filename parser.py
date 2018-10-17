""" Entities parser """


def parse_intent(request):
    """ Parses extracted entities from Dialogflow build_intent request """

    result = request["queryResult"]
    entities = {}
    entities["id"] = result["intent"]["displayName"]

    parameters = result["parameters"]

    if parameters["origin"]:
        entities["origin"] = parameters["origin"]
        if isinstance(entities["origin"], dict):
            entities["origin"] = next(iter(parameters["origin"].values()), "").strip()

    if parameters["destination"]:
        entities["destination"] = parameters["destination"]
        if isinstance(entities["destination"], dict):
            entities["destination"] = next(iter(parameters["destination"].values()), "").strip()

    if parameters["target"]:
        entities["targets"] = parameters["target"]

    if parameters["middlebox"]:
        entities["middleboxes"] = parameters["middlebox"]

    if parameters["qos_metric"] and parameters["qos_constraint"] and parameters["qos_value"] and parameters["qos_unit"]:
        entities["qos"] = []
        qos_metrics = parameters["qos_metric"]
        qos_constraints = parameters["qos_constraint"]
        qos_values = parameters["qos_value"]
        qos_units = parameters["qos_unit"]
        for idx, qos_metric in enumerate(qos_metrics):
            metric = {}
            metric["name"] = qos_metric
            metric["constraint"] = qos_constraints[idx]
            metric["value"] = qos_values[idx] if isinstance(qos_values[idx], str) else str(qos_values[idx]["qos_value"]["number-integer"])
            metric["unit"] = qos_units[idx]["qos_unit"]
            entities["qos"].append(metric)

    if parameters["start"]:
        entities["start"] = parameters["start"]
        if isinstance(entities["start"], dict):
            entities["start"] = next(iter(parameters["start"].values()), "").strip()

    if parameters["end"]:
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
