import numpy as np

import dataset
import model

if __name__ == "__main__":
    input_words, output_words = dataset.read()

    # Creating the network model
    print('[INFO] Compiling model...')
    model = model.AttentionSeq2Seq(input_words, output_words)
    # model.train()
    model.test()
