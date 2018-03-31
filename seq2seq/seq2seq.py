import numpy as np

import dataset
import encoding
import model

train = True
test = True

seq2seq = None


def deanonymize(intent, id, origin, destination, targets, middleboxes, qos, start, end, allow, block):
    intent = intent.replace('@id', id)
    intent = intent.replace('@location', origin, 1) if origin is not None else intent
    intent = intent.replace('@location', destination, 1) if destination is not None else intent

    if targets is not None:
        for target in targets:
            intent = intent.replace('@target', target, 1)

    if middleboxes is not None:
        for mb in middleboxes:
            intent = intent.replace('@middlebox', mb, 1)

    if qos is not None:
        for metric in qos:
            intent = intent.replace('@qos_metric', metric['name'], 1)
            intent = intent.replace('@qos_constraint', metric['constraint'], 1)
            if metric['value']:
                intent = intent.replace('@qos_value', metric['value'], 1)

    intent = intent.replace('@hour', start) if start is not None else intent
    intent = intent.replace('@hour', end) if end is not None else intent

    intent = intent.replace('@traffic', end) if allow is not None else intent
    intent = intent.replace('@traffic', end) if block is not None else intent

    return intent


def anonymize(id, origin, destination, targets, middleboxes, qos, start, end, allow, block):
    entities = '@id '
    entities += '@location ' if origin is not None else ''
    entities += '@location ' if destination is not None else ''

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

    entities += '@hour ' if start is not None else ''
    entities += '@hour ' if end is not None else ''

    entities += 'allow @traffic ' if allow is not None else ''
    entities += 'block @traffic ' if block is not None else ''

    return entities.strip()


def translate(id, origin, destination, targets, middleboxes, qos, start, end, allow, block):
    global seq2seq
    entities = anonymize(id, origin, destination, targets, middleboxes, qos, start, end, allow, block)
    print('entities', entities)
    intent, rsquared = seq2seq.predict(entities)
    print('intent', intent)
    result = deanonymize(intent, id, origin, destination, targets, middleboxes, qos, start, end, allow, block)
    print('result', result)

    return result


def init():
    global seq2seq, train, test
    fit_input_words, fit_output_words = dataset.read('fit')
    test_input_words, test_output_words = dataset.read('test')

    # Creating the network model
    seq2seq = model.AttentionSeq2Seq(fit_input_words, fit_output_words)
    if train:
        seq2seq.train(fit_input_words, fit_output_words)
        train = False

    if test:
        rsquared_list = seq2seq.test(test_input_words, test_output_words)
        print("R-squared: {}".format(rsquared_list))


def feedback():
    global seq2seq
    test_input_words, test_output_words = dataset.read('feedback')

    rsquared_list = []
    for index, test_input, test_output in enumerate(zip(test_input_words, test_output_words)):
        print('entities', test_input)
        intent, rsquared = seq2seq.predict(test_input, test_output)
        print('intent: {}, rsquared: {}'.format(test_output, rsquared))
        rsquared_list.append([index, rsquared]);


    with open("res/dataset_{}/feedback_results.csv".format(config.FIT_DATASET_SIZE), "wb") as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerow(['id', 'rsquared'])
        for row in rsquared_list:
            writer.writerow(row)




if __name__ == "__main__":
    init()
    print(translate("asjacobs", "backend", "office", ["University"], ["firewall", "vpn"], None, None, None, None, None))
