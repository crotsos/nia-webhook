import os

import numpy as np
import scipy

import config
import encoding

from sklearn.metrics import r2_score

from keras.layers import (Activation, Dense, Embedding, RepeatVector,
                          TimeDistributed, recurrent)
from keras.layers.recurrent import LSTM
from keras.models import Sequential
from keras.optimizers import Adam, RMSprop
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import text_to_word_sequence


class AttentionSeq2Seq:
    def __init__(self, input_words, output_words):
        self.input_index_to_word, self.input_word_to_index = encoding.build_index(input_words)
        self.output_index_to_word, self.output_word_to_index = encoding.build_index(output_words)

        self.input_vocab_len = encoding.get_vocab_size(input_words)
        self.input_max_len = max([len(sentence) for sentence in input_words])
        self.output_vocab_len = encoding.get_vocab_size(output_words)
        self.output_max_len = max([len(sentence) for sentence in output_words])


        print('[INFO] Creating model...')
        self.model = Sequential()

        print('[INFO] Creating encoder...')
        # Creating encoder network
        self.model.add(Embedding(self.input_vocab_len, 1000, input_length=self.input_max_len, mask_zero=True))
        self.model.add(LSTM(config.MODEL_HIDDEN_DIM))

        print('[INFO] Creating decoder...')
        # Creating decoder network
        self.model.add(RepeatVector(self.output_max_len))
        for i in range(config.MODEL_HIDDEN_LAYERS):
            self.model.add(LSTM(config.MODEL_HIDDEN_DIM, return_sequences=True))
        self.model.add(TimeDistributed(Dense(self.output_vocab_len)))
        self.model.add(Activation(config.MODEL_ACTIVATION))

        print('[INFO] Compiling model...')
        self.model.compile(loss=config.MODEL_LOSS, optimizer=config.MODEL_OPTIMIZER,  metrics=config.MODEL_METRICS)

    def train(self, input_words, output_words, index=True):
        k_start = self.load();

        if index:
            input_words = encoding.index(input_words, self.input_word_to_index)
            output_words = encoding.index(output_words, self.output_word_to_index)

        # Zero padding
        input_words = pad_sequences(input_words, maxlen=self.input_max_len, dtype='int32')
        output_words = pad_sequences(output_words, maxlen=self.output_max_len, dtype='int32')

        print('[INFO] Training... starting epoch: {}'.format(k_start))
        i_end = 0
        for k in range(k_start, config.MODEL_EPOCHS + 1):
            # Shuffling the training data every epoch to avoid local minima
            indices = np.arange(len(input_words))
            np.random.shuffle(indices)
            input_words = input_words[indices]
            output_words = output_words[indices]

            # Training 5000 sequences at a time
            for i in range(0, len(input_words), 5000):
                if i + 5000 >= len(input_words):
                    i_end = len(input_words)
                else:
                    i_end = i + 5000
                output_sequences = encoding.vectorize(output_words[i:i_end], self.output_max_len, self.output_word_to_index)

                print('[INFO] Training model: epoch {}th {}/{} samples'.format(k, i, len(input_words)))
                self.model.fit(input_words[i:i_end], output_sequences, batch_size=config.MODEL_BATCH_SIZE, validation_split=config.MODEL_VALIDATION_SPLIT, epochs=1, verbose=2)
            self.model.save_weights(config.MODEL_WEIGHTS_PATH.format(config.FIT_DATASET_SIZE, k))

    def test(self, input_words, output_words):
        self.load();

        if len(self.saved_weights) == 0:
            print("The network hasn't been trained! Program will exit...")
            exit()
        else:
            print('[INFO] Testing...')
            input_words = encoding.index(input_words, self.input_word_to_index)
            output_words = encoding.index(output_words, self.output_word_to_index)

            input_words = pad_sequences(input_words, maxlen=self.input_max_len, dtype='int32')
            output_words = pad_sequences(output_words, maxlen=self.output_max_len, dtype='int32')

            predictions = np.argmax(self.model.predict(input_words), axis=2)

            inputs = []
            outputs = []
            rsquared_list = []
            for input_sequence, output_sequence, prediction in zip(input_words, output_words, predictions):
                entities = ' '.join([self.input_index_to_word[index] for index in input_sequence if index > 0])
                sequence = ' '.join([self.output_index_to_word[index] for index in prediction if index > 0])
                inputs.append(entities)
                outputs.append(sequence)
                print("expected: {}".format(output_sequence))
                print("predicted: {}".format(prediction))
                rsquared_list.append(np.corrcoef(output_sequence, prediction))

            np.savetxt(config.MODEL_TEST_INPUT_PATH.format(config.FIT_DATASET_SIZE), inputs, fmt='%s')
            np.savetxt(config.MODEL_TEST_RESULT_PATH.format(config.FIT_DATASET_SIZE), outputs, fmt='%s')

            return r2_score(output_words, predictions, multioutput='variance_weighted')

    def predict(self, entities, expected_intent=None):
        intent = ''
        r2_score = 0
        self.load();

        if len(self.saved_weights) == 0:
            print("The network hasn't been trained! Program will exit...")
        else:
            print('[INFO] Predicting...')

            entities = [text_to_word_sequence(entities, filters=config.DATASET_FILTERS) if not isinstance(entities, list) else entities]
            entities = encoding.index(entities, self.input_word_to_index)
            entities = pad_sequences(entities, maxlen=self.input_max_len, dtype='int32')
            if expected_intent:
                expected_intent = [text_to_word_sequence(expected_intent, filters=config.DATASET_FILTERS) if not isinstance(expected_intent, list) else expected_intent]
                expected_intent = encoding.index(expected_intent, self.output_word_to_index)
                expected_intent = pad_sequences(expected_intent, maxlen=self.output_max_len, dtype='int32')[0]

            prediction = np.argmax(self.model.predict(entities), axis=2)[0]
            intent = ' '.join([self.output_index_to_word[index] for index in prediction if index > 0])

            r2_score = rsquared(expected_intent, prediction) if expected_intent is not None else 0
        return intent, r2_score

    def load(self):
        epoch = 1
        self.saved_weights = find_checkpoint_file()
        if len(self.saved_weights) != 0:
            print('[INFO] Saved weights found, loading...', self.saved_weights)
            epoch = self.saved_weights[self.saved_weights.rfind('_') + 1:self.saved_weights.rfind('.')]
            self.model.load_weights(self.saved_weights)
        return int(epoch)

def rsquared(x, y):
    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x, y)
    return r_value**2

def find_checkpoint_file():
    checkpoint_file = [config.MODEL_DIR.format(config.FIT_DATASET_SIZE) + f for f in os.listdir(config.MODEL_DIR.format(config.FIT_DATASET_SIZE)) if 'weights' in f]
    if len(checkpoint_file) == 0:
        return []
    modified_time = [os.path.getmtime(f) for f in checkpoint_file]
    return checkpoint_file[np.argmax(modified_time)]
