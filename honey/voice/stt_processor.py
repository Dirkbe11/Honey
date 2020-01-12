import numpy as np
import deepspeech as ds
import numpy as np
import audioop

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

from timeit import default_timer as timer
from .text_processor import *

class STTProcesser():
    def __init__(self, output_function):
        print("+Loading STT Processor...")
        load_start = timer()
        self.LM_WEIGHT = .25
        self.LM_INSERTION_BONUS = 2.20
        self.BEAM_WIDTH = 2048
        self.model_path = "honey/voice/deepspeech-0.6.0-models/output_graph.pbmm"
        self.language_model_path = 'honey/voice/deepspeech-0.6.0-models/lm.binary'
        self.trie_path = 'honey/voice/deepspeech-0.6.0-models/trie'

        #Create new model
        self.model = ds.Model(self.model_path, self.BEAM_WIDTH)
        #Add trie and language model to Model
        self.model.enableDecoderWithLM(self.language_model_path, self.trie_path, self.LM_WEIGHT, self.LM_INSERTION_BONUS)

        self.text_processor = TextProcessor(output_function)
        
        load_end = timer() - load_start
        print("...STT Processor loaded in {}".format(load_end))

        print("+Loading Google STT...")
        load_start = timer()

        self.google_stt_client = speech.SpeechClient()
        
        self.config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=48000,
        language_code='en-US',
        model='command_and_search')

        load_end = timer() - load_start
        print("...STT Processor loaded in {}".format(load_end))

        

    def ProcessSpeech(self, user, data):
        
        #prep data
        reduced_sample_ratedata = audioop.ratecv(data, 2, 2, 48000, 16000, None)
        mono_data = audioop.tomono(reduced_sample_ratedata[0], 2, 1, 0)
        voice_data = np.fromstring(mono_data, np.int16)

        #run initial deepspeech conversion
        text = self.model.stt(voice_data)

        #check for honey keyword
        honey_activated = self.text_processor.process_initial(user, text)

        if(honey_activated == True and len(text) > 12):
            print("HONEY FOUND")
            print("text: {}".format(text))
            google_mono_data = audioop.tomono(data, 2, 1, 0)
            audio = types.RecognitionAudio(content=google_mono_data)
            print("audio")
            candidate_command = self.google_stt_client.recognize(config=self.config, audio=audio)
            print("\n\nGOOGLE: {}\n\n".format(candidate_command))
            print("TRANSCRIPT: {}".format(candidate_command.results[0].alternatives[0].transcript))
            print("confidence: {}".format(candidate_command.results[0].alternatives[0].confidence))
           
            self.text_processor.ProcessText(candidate_command.results[0].alternatives[0].transcript.lower(), user)


