import numpy as np
import deepspeech as ds
import numpy as np
import audioop
import sys
from multiprocessing import Pool
from threading import Lock

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

from timeit import default_timer as timer
from .text_processor import *


#==============================================
#performs the deepspeech screening
#==============================================
def deepspeech_screen(data, user):
    reduced_sample_ratedata = audioop.ratecv(data, 2, 2, 48000, 16000, None)
    mono_data = audioop.tomono(reduced_sample_ratedata[0], 2, 1, 0)
    voice_data = np.fromstring(mono_data, np.int16)

    print("deepspeech pre")
    text = model.stt(voice_data)
    print("deepspeech post")
    result = [user, text, data]

    return result

    
class STTProcesser():
    def __init__(self, output_function):
        self.text_processor = TextProcessor(output_function)

        #load google STT
        print("+Loading Google STT...")
        load_start = timer()
        self.GSTT_lock = Lock()
        self.google_stt_client = speech.SpeechClient()

        self.config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=48000,
        language_code='en-US',
        model='command_and_search')

        load_end = timer() - load_start
        print("...Google STT loaded in {}".format(load_end))

        #set up worker pool
        print("+Loading STT worker pool...")
        load_start = timer()
        self.worker_pool = Pool(4, self.worker_pool_initializer, ())
        load_end = timer() - load_start
        print("...STT worker pool loaded in {}".format(load_end))


    #==============================================
    #Initialize each worker process with their own deepspeech model
    #==============================================
    def worker_pool_initializer(self):
        global model
        # global text_processor

        #Build model
        LM_WEIGHT = .25
        LM_INSERTION_BONUS = 2.20
        BEAM_WIDTH = 2048
        model_path = "honey/voice/deepspeech-0.6.0-models/output_graph.pbmm"
        language_model_path = 'honey/voice/deepspeech-0.6.0-models/lm.binary'
        trie_path = 'honey/voice/deepspeech-0.6.0-models/trie'#Create new model
        model = ds.Model(model_path, BEAM_WIDTH)#Add trie and language model to Model
        model.enableDecoderWithLM(language_model_path, trie_path, LM_WEIGHT, LM_INSERTION_BONUS)

        #TODO: Add a way for each process to share a user dictionary so they can
        #search deepspeech text in parallel...
        # text_processor = TextProcessor(output_function)

    #==============================================
    #runs the initial deepspeech screen
    #==============================================
    def ProcessSpeech(self, user, data):
        #transfer data to immutable type so we can pass to worker process
        new_data = bytes(data)
        #run initial deepspeech screen in seperate process
        self.worker_pool.apply_async(deepspeech_screen, [new_data, user], callback=self.stage_two)

    #==============================================
    #If honey was found, send data to google STT and handle results
    #==============================================
    def stage_two(self, result):
        print("\n RESULT: {}\n".format(result[1]))

        self.GSTT_lock.acquire()
        stage_one_result = self.text_processor.process_initial(result[0], result[1])

        if(stage_one_result == True and len(result[1]) > 12):
            google_mono_data = audioop.tomono(result[2], 2, 1, 0)
            audio = types.RecognitionAudio(content=google_mono_data)
            candidate_command = self.google_stt_client.recognize(config=self.config, audio=audio)
            print("\n\nGOOGLE: {}\n\n".format(candidate_command))
            self.text_processor.ProcessText(candidate_command.results[0].alternatives[0].transcript.lower(), result[0])
        self.GSTT_lock.release()
