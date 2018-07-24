import csv
import time

import config
import dataset
import encoding
import model

train = False
test = True

seq2seq = None
fit_input_words = []
fit_output_words = []


def deanonymize(intent, id, origin, destination, targets, middleboxes, qos, start, end, allow, block):
    intent = intent.replace('@id', id, 1)
    intent = intent.replace('@location', origin, 1) if origin is not None else intent
    intent = intent.replace('@location', destination, 1) if destination is not None else intent

    if targets is not None:
        for target in targets:
            intent = intent.replace('@target', target.strip(), 1)

    if middleboxes is not None:
        for mb in middleboxes:
            intent = intent.replace('@middlebox', mb.strip(), 1)

    if qos is not None:
        for metric in qos:
            intent = intent.replace('@qos_metric', metric['name'], 1)
            intent = intent.replace('@qos_constraint', metric['constraint'], 1)
            if metric['value']:
                intent = intent.replace('@qos_value', metric['value'], 1)

    intent = intent.replace('@hour', start, 1) if start is not None else intent
    intent = intent.replace('@hour', end, 1) if end is not None else intent

    intent = intent.replace('@traffic', allow, 1) if allow is not None else intent
    intent = intent.replace('@traffic', block, 1) if block is not None else intent

    return intent


def anonymize(id, origin, destination, targets, middleboxes, qos, start, end, allow, block):
    entities = '@id '
    entities += '@location ' if origin is not None and origin else ''
    entities += '@location ' if destination is not None and destination else ''

    if targets is not None:
        for target in targets:
            entities += '@target '

    if middleboxes is not None:
        for mb in middleboxes:
            entities += '@middlebox '

    if qos is not None:
        for metric in qos:
            entities += '@qos_metric ' + '@qos_constraint '
            if metric['value']:
                entities += '@qos_value'

    entities += '@hour ' if start is not None and start else ''
    entities += '@hour ' if end is not None and end else ''

    entities += 'allow @traffic ' if allow is not None else ''
    entities += 'block @traffic ' if block is not None else ''

    return entities.strip()

def entity_nile_translate(entities):
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
    if '@qos_metric' in entity_dict and  '@qos_constraint' in entity_dict and '@qos_value' in entity_dict:
        result += "with @qos_metric('@qos_constraint','@qos_value')"
    return result

def translate(id, origin, destination, targets, middleboxes, qos, start, end, allow, block):
    global seq2seq
    entities = anonymize(id, origin, destination, targets, middleboxes, qos, start, end, allow, block)
    print('entities', entities)
    #intent, rsquared = seq2seq.predict(entities)
    intent = entity_nile_translate(entities)
    print('intent', intent)
    result = deanonymize(intent, id, origin, destination, targets, middleboxes, qos, start, end, allow, block)
    print('result', result)

    return result


def init():
    global seq2seq, train, test, fit_input_words, fit_output_words
    fit_input_words, fit_output_words = dataset.read('fit')
    test_input_words, test_output_words = dataset.read('test')
    # Creating the network model
    seq2seq = model.AttentionSeq2Seq(fit_input_words, fit_output_words)
    if train:
        seq2seq.train(fit_input_words, fit_output_words)
        train = False

    if test:
        (rsquared_mean, confidence_bottom, confidence_top) = seq2seq.test(test_input_words, test_output_words)
        print("R-squared: {}, {}, {}".format(rsquared_mean, confidence_bottom, confidence_top))
        with open(config.RESULTS_PATH, "a") as file:
            writer = csv.writer(file, delimiter=",")
            writer.writerow([config.FIT_DATASET_SIZE, rsquared_mean, confidence_bottom, confidence_top])


def feedback():
    global seq2seq, fit_input_words, fit_output_words
    test_input_words, test_output_words = dataset.read('feedback')

    with open(config.FEEDBACK_PATH.format(config.FIT_DATASET_SIZE), "wb") as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerow(['id', 'rsquared'])

        for index, (test_input, test_output) in enumerate(zip(test_input_words, test_output_words)):
            intent, rsquared = seq2seq.predict(test_input, test_output)
            print('intent: {}, rsquared: {}'.format(test_output, rsquared))
            writer.writerow([index, rsquared])
            fit_input_words.append(test_input)
            fit_output_words.append(test_output)
            seq2seq.train(fit_input_words, fit_output_words, False)


def time_test():
    global seq2seq
    time_input_words, time_output_words = dataset.read('time')

    with open("../res/dataset_{}/time_results.csv".format(config.FIT_DATASET_SIZE), "wb") as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerow(['num', 'time'])

        for time_input in time_input_words:
            start = time.time()
            print('entities', time_input)
            intent, rsquared = seq2seq.predict(time_input)
            end = time.time()
            m_time = end - start
            length = len(time_input)
            print('intent: {}, length: {}, time: {}'.format(intent, length, m_time))
            writer.writerow([length, m_time])


if __name__ == "__main__":
    init()
    # feedback()
    print(translate("asjacobs", "client", "server", None, ["firewall", "ids"], None, None, None, None, None))
