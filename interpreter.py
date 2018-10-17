""" Nile interpreter """


def translate(entities):
    """ Translates extracted entities into a Nile intent """

    intent = "define intent {}Intent: ".format(entities["id"])

    if "origin" in entities and "destination" in entities:
        intent += "from endpoint('{}') to endpoint('{}') ".format(entities["origin"], entities["destination"])
    elif ("origin" in entities and "destination" not in entities) or \
            ("origin" not in entities and "destination" in entities):
        raise ValueError("Origin cannot be used without destination, and vice-versa.")

    if "targets" in entities:
        intent += "for"
        for target in entities["targets"]:
            intent += " client('{}'),".format(target)
        intent = intent.rstrip(',')

    if "middleboxes" in entities:
        intent += "add"
        for middlebox in entities["middleboxes"]:
            intent += " middlebox('{}'),".format(middlebox)
        intent = intent.rstrip(',')

    if "qos" in entities:
        intent += "set"
        for metric in entities["qos"]:
            if "name" in metric and "constraint" in metric and "value" in metric:
                intent += " @qos_metric('@qos_constraint','@qos_value'),"
            else:
                raise ValueError("Missing qos metric parameters.")
        intent = intent.rstrip(',')

    if "start" in entities and "end" in entities:
        intent += "start hour('{}') to hour('{}') ".format(entities["start"], entities["end"])
    elif ("start" in entities and "end" not in entities) or \
            ("start" not in entities and "end" in entities):
        raise ValueError("Start cannot be used without end, and vice-versa.")

    return intent
