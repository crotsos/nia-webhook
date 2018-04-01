from random import randint, sample

import config
from keras.preprocessing.text import text_to_word_sequence

def get_intent(id, origin, destination, targets, middleboxes, qos, start, end, allow, block):
    intent = 'define intent ' + id + 'Intent:'
    if origin:
        intent = intent + ' from endpoint("' + origin + '")'
    if destination:
        intent = intent + ' to endpoint("' + destination + '")'

    for index, target in enumerate(targets):
        if target:
            if 'for' not in intent:
                intent = intent + ' for '
            intent = intent + 'client("' + target + '")'

            if index != (len(targets) - 1):
                intent = intent + ', '

    for index, mb in enumerate(middleboxes):
        if mb:
            if 'add' not in intent:
                intent = intent + ' add '
            intent = intent + 'middlebox("' + mb + '")'

            if index != (len(middleboxes) - 1):
                intent = intent + ', '

    for index, metric in enumerate(qos):
        if metric and metric['name'] not in intent:
            if 'with' not in intent:
                intent = intent + ' with '

            intent = intent + metric['name'] + '("' + metric['constraint']
            intent = intent + '","' + metric['value'] + '")' if metric['value'] else intent + '")'

            if index != (len(qos) - 1):
                intent = intent + ', '

    if start:
        intent = intent + ' start hour("' + start + '")'
    if end:
        intent = intent + ' end hour("' + end + '")'

    if allow:
        if allow not in intent:
            intent = intent + ' allow trafic("' + allow + '")'
    if block:
        if block not in intent:
            intent = intent + ' block trafic("' + block + '")'

    return intent

def get_entities(id, origin, destination, targets, middleboxes, qos, start, end, allow, block):
    entities = id
    if origin:
        entities = entities + ' ' + origin
    if destination:
        entities = entities + ' ' + destination

    for target in targets:
        if target:
            entities = entities + ' ' + target

    for mb in middleboxes:
        if mb:
            entities = entities + ' ' + mb

    for metric in qos:
        if metric:
            if metric['name'] not in entities:
                entities = entities + ' ' + metric['name'] + ' ' + metric['constraint']
                if metric['value']:
                    entities = entities + ' ' + metric['value']

    if start:
        entities = entities + ' ' + start
    if end:
        entities = entities + ' ' + end

    if allow:
        if allow not in entities:
            entities = entities + ' allow ' + allow
    if block:
        if block not in entities:
            entities = entities + ' block ' + block

    return entities

def write(dataset_type):
    dataset_sizes = {
        'fit': config.FIT_DATASET_SIZE,
        'test': config.TEST_DATASET_SIZE,
        'feedback':  config.FEEDBACK_DATASET_SIZE,
    }
    dataset_size = dataset_sizes[dataset_type]
    with open(config.DATASET_PATH.format(config.FIT_DATASET_SIZE, dataset_type), 'wb') as file:
        for i in range(dataset_size):
            qos = []
            for metric in range(randint(0, 2)):
                qos.append({'name': '@qos_metric', 'constraint': '@qos_constraint', 'value': '@qos_value' if randint(0, 10) % 2 == 0 else None})

            id = '@id'
            origin = '@location' if randint(0, 10) % 2 == 0 else None
            destination = '@location' if randint(0, 10) % 2 == 0 else None
            target = ['@target' for i in range(randint(0, 2))]
            mbs = ['@middlebox' for i in range(randint(0, 2))]
            start = '@hour' if randint(0, 10) % 2 == 0 else None
            end = '@hour' if start else None
            allow = '@traffic' if randint(0, 10) % 2 == 0 else None
            block = '@traffic' if randint(0, 10) % 2 == 0 else None
            entities = get_entities(id, origin, destination, target, mbs, qos, start, end, allow, block)
            intent = get_intent(id, origin, destination, target, mbs, qos, start, end, allow, block)
            file.write(entities + ' > ' + intent + '\n')


def write_time():
    entities_intent = {}
    for metric_i in range(0,5):
        for value in range(0,2):
            qos = [{'name': '@qos_metric', 'constraint': '@qos_constraint', 'value': '@qos_value' if value == 0 else None} for i in range(metric_i)]
            id = '@id'
            for origin_i in range(0,2):
                origin = '@location' if origin_i == 0 else None
                for destination_i in range(0,2):
                    destination = '@location' if destination_i == 0 else None
                    for target_i in range(4):
                        target = ['@target' for i in range(target_i)]
                        for mb_i in range(6):
                            mbs = ['@middlebox' for i in range(mb_i)]
                            for start_i in range(0,2):
                                start = '@hour' if start_i == 0 else None
                                end = '@hour' if start else None
                                for allow_i in range(0,2):
                                    allow = '@traffic' if allow_i == 0 else None
                                    for block_i in range(0,2):
                                        block = '@traffic' if block_i == 0 else None
                                        entities = get_entities(id, origin, destination, target, mbs, qos, start, end, allow, block)
                                        intent = get_intent(id, origin, destination, target, mbs, qos, start, end, allow, block)
                                        if len(entities.split(" ")) > 1:
                                            entities_intent[len(entities.split(" "))] = (entities, intent)

    with open(config.DATASET_PATH.format(config.FIT_DATASET_SIZE, "time"), 'wb') as file:
        min_key = 1000
        max_key = 0
        for length, (entities, intent) in entities_intent.items():
            min_key = length if min_key > length else min_key
            max_key = length if max_key < length else max_key
            file.write(entities + ' > ' + intent + '\n')
        print("min {}, max {}".format(min_key, max_key))

def read(type):
    lines = []

    input_words = []
    output_words = []

    with open(config.DATASET_PATH.format(config.FIT_DATASET_SIZE, type), 'r') as f:
        lines = f.read().split('\n')

    for line in lines:
        if line and not line.startswith('#'):
            input_text, output_text = line.split('>')
            input_words.append(text_to_word_sequence(input_text, filters=config.DATASET_FILTERS))
            output_words.append(text_to_word_sequence(output_text, filters=config.DATASET_FILTERS))

    return input_words, output_words

if __name__ == "__main__":
    write('fit')
    write('test')
    write('feedback')
    write_time()
