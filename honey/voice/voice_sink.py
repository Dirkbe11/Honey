import asyncio
import wave
import discord

from discord.rtp import SilencePacket
from .stt_processor import STTProcesser

class VoiceSink(discord.reader.AudioSink):
    def __init__(self, output_function):
        self.stt_processor = STTProcesser(output_function)
        self.user_data_buffer = {}

    def write(self, packet):
        #add new user

        if not (packet.user in self.user_data_buffer):
            self.user_data_buffer[packet.user] = [0, bytearray()]
            self.user_data_buffer[packet.user][1] += packet.data

        if not (type(packet.packet) is SilencePacket) and len(self.user_data_buffer[packet.user][1]) < 3000000:
            self.user_data_buffer[packet.user][1] += packet.data
            self.user_data_buffer[packet.user][0] = 0
        else:
            self.user_data_buffer[packet.user][0] += 1
            if self.user_data_buffer[packet.user][0] > 25:
                self.user_data_buffer[packet.user][0] = 0

                if(len(self.user_data_buffer[packet.user][1]) != 0):
                    voice_data = self.user_data_buffer[packet.user][1]
                    self.stt_processor.ProcessSpeech(packet.user.id, voice_data)
                    self.user_data_buffer[packet.user][1].clear()


    def cutbuffer(self, idx):
        self.byte_array_buffer = self.byte_array_buffer[idx:]
