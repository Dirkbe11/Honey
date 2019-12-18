import asyncio

class VoiceSink():
    def __init__(self):
        self.byte_array_buffer = bytearray()
		# sample width, which is (bit_rate/8) * channels
        self.sample_width = 2
		# 48000Hz sampling rate
		# doubled, because speech_recognition needs mono and we've got stereo
        self.sample_rate = 96000
		# calculated bytes per second, sample_rate * sample_width
		# we need this to know what slices we can take from the buffer
		# would be 96000, but mono
        self.bytes_ps = 192000

    #append data to the byte array buffer
    def write(self, data):
        self.byte_array_buffer += data.data

    def cutbuffer(self, idx):
        self.byte_array_buffer = self.byte_array_buffer[idx:]


        
