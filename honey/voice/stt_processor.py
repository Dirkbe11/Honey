import numpy as np
import deepspeech as ds

from timeit import default_timer as timer
class STTProcesser():
    def __init__(self):
        self.LM_WEIGHT = .75#1.5
        self.LM_INSERTION_BONUS = 1.85
        self.VALID_WORD_COUNT_WEIGHT = 2.25
        self.N_FEATURES = 26
        self.N_CONTEXT = 9
        self.BEAM_WIDTH = 500
        self.model_path = "honey/voice/deepspeech-0.6.0-models/output_graph.pbmm"
        self.language_model_path = 'honey/voice/deepspeech-0.6.0-models/lm.binary'
        self.trie_path = 'honey/voice/deepspeech-0.6.0-models/trie'

        #Create new model
        print('Loading model...')
        model_load_start = timer()
        self.model = ds.Model(self.model_path, self.BEAM_WIDTH)
        model_load_end = timer() - model_load_start
        print('Model loaded in {}s.'.format(model_load_end))
        
        #Add trie and language model to Model
        print('Loading language model...')
        model_load_start = timer()
        self.model.enableDecoderWithLM(self.language_model_path, self.trie_path, self.LM_WEIGHT, self.LM_INSERTION_BONUS)
        model_load_end = timer() - model_load_start
        print('Language Model loaded in {}s.'.format(model_load_end))

        desired_sample_rate = self.model.sampleRate()
        print("DESIRED RATE: {}".format(desired_sample_rate))

    def Process(self, data):
        print("processing text!")
        print(self.model.stt(data))
        print("should have processed")
