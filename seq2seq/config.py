import os
import sys

ROOT_PATH = os.path.dirname(sys.modules['__main__'].__file__)

############ DATASET ############
DATASET_PATH = os.path.join(ROOT_PATH, 'res/dataset_{}/{}_dataset.txt')
RESULTS_PATH = os.path.join(ROOT_PATH, 'res/dataset_results.csv')
FEEDBACK_PATH = os.path.join(ROOT_PATH, 'res/dataset_{}/feedback_results.csv')
FIT_DATASET_SIZE = 5000
TEST_DATASET_SIZE = 1000
FEEDBACK_DATASET_SIZE = 30
DATASET_VOCAB_SIZE = 2000
DATASET_FILTERS = '!$&*+-./;<=>?#[\\]^{|}~\t\n'

############ MODEL ############
MODEL_DIR = os.path.join(ROOT_PATH, 'res/dataset_{}/weights/')
MODEL_TEST_INPUT_PATH = os.path.join(ROOT_PATH, 'res/dataset_{}/test_input.txt')
MODEL_TEST_RESULT_PATH = os.path.join(ROOT_PATH, 'res/dataset_{}/test_result.txt')
MODEL_WEIGHTS_PATH = os.path.join(ROOT_PATH, 'res/dataset_{}/weights/model_weights_{}.hdf5')

MODEL_ACTIVATION = 'softmax'
MODEL_OPTIMIZER = 'adam'
MODEL_METRICS = ['accuracy']
MODEL_LOSS = 'categorical_crossentropy'

MODEL_BATCH_SIZE = 64         # Batch size for training.
MODEL_EPOCHS = 70             # Number of epochs to train for.
MODEL_LATENT_DIM = 256        # Latent dimensionality of the encoding space.
MODEL_HIDDEN_DIM = 1000       # Dimensionality of hidden layer.
MODEL_HIDDEN_LAYERS = 3       # Number of hidden layers.
MODEL_VALIDATION_SPLIT = 0.2  # Fraction of dataset used to validate model fitting.
