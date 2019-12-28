import asyncio
import wave
import discord
import numpy as np
import audioop

from discord.rtp import SilencePacket
from .stt_processor import STTProcesser

class VoiceSink(discord.reader.AudioSink):
    def __init__(self):
        self.byte_array_buffer = bytearray()
		# sample width, which is (bit_rate/8) * channels
        self.sample_width = 2

		# 48000Hz sampling rate
		# doubled, because speech_recognition needs mono and we've got stereo
        self.sample_rate = 96000 #DIRK: Audio signals are continous, but we need
        #a discrete representation of them. The sample_rate is how many samples per
        #second we take from the continous audio source in order to make it discrete.

		# calculated bytes per second, sample_rate * sample_width
		# we need this to know what slices we can take from the buffer
		# would be 96000, but mono
        self.bytes_ps = 192000

        self.stt_processor = STTProcesser()

        self.actionflag = True
        self.num = 0
    
    def write(self, packet):
        #filter silence packets

        if not type(packet.packet) is SilencePacket:
            print(self.num)
            self.num = self.num + 1
            self.byte_array_buffer += packet.data

            if len(self.byte_array_buffer) > 550000:
                data = audioop.ratecv(self.byte_array_buffer, 2, 2, 48000, 16000, None)
                data = audioop.tomono(data[0], 2, 1, 0)
                voice_data = np.fromstring(data, np.int16)
                # self.stt_processor.ProcessSpeech(packet.user.id, voice_data)
                self.byte_array_buffer.clear()


    def cutbuffer(self, idx):
        self.byte_array_buffer = self.byte_array_buffer[idx:]


        


#GRAVEYARD:
      # #will probably wanty to get rid of this
        # self._file = wave.open('sound.wav', 'wb')
        # self._file.setnchannels(2)
        # self._file.setsampwidth(2)
        # self._file.setframerate(48000)
        # self.actionflag = True