
def translate(entities):
    result = 'define intent @idintent: '
    entity_list = entities.split(' ')
    entity_dict = {}
    for e in entity_list:
        if e in entity_dict:
            entity_dict[e] += 1
        else:
            entity_dict[e] = 1
    if '@target' in entity_dict:
        result += "for client('@target') "
    if '@location' in entity_dict and entity_dict['@location'] == 2:
        result += "from endpoint('@location') to endpoint('@location') "
    if '@middlebox' in entity_dict:
        result += 'add'
        for i in range(entity_dict['@middlebox']):
            result += " middlebox('@middlebox'),"
        result = ' '.join(result.rsplit(',', 1))
    if '@qos_metric' in entity_dict and '@qos_constraint' in entity_dict and '@qos_value' in entity_dict:
        result += "with @qos_metric('@qos_constraint','@qos_value')"
    return result
