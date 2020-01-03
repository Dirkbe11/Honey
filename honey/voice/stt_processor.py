import numpy as np
import deepspeech as ds

from timeit import default_timer as timer
from .text_processor import *

class STTProcesser():
    def __init__(self, output_function):
        print("+Loading STT Processor...")
        load_start = timer()
        self.LM_WEIGHT = .75#1.5
        self.LM_INSERTION_BONUS = 1.85
        self.BEAM_WIDTH = 1024
        self.model_path = "honey/voice/deepspeech-0.6.0-models/output_graph.pbmm"
        self.language_model_path = 'honey/voice/deepspeech-0.6.0-models/lm.binary'
        self.trie_path = 'honey/voice/deepspeech-0.6.0-models/trie'

        #Create new model
        self.model = ds.Model(self.model_path, self.BEAM_WIDTH)
        #Add trie and language model to Model
        self.model.enableDecoderWithLM(self.language_model_path, self.trie_path, self.LM_WEIGHT, self.LM_INSERTION_BONUS)

        self.text_processor = TextProcessor(output_function)

        load_end = timer() - load_start
        print("STT Processor loaded in {}".format(load_end))

    def ProcessSpeech(self, user, data):
        text = self.model.stt(data)
        self.text_processor.Process(user, text)
