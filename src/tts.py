# Copyright (c) 2025 Punchnox
# https://github.com/notpunchnox
# LICENSE MIT

# Import libraries
import requests
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play
from piper.voice import PiperVoice
import wave
import os

model = "./ressources/voice/fr_FR-tom-medium.onnx"
voice = PiperVoice.load(model)

def sendTTS(content, args):
    output_file = "output.wav"
    
    with wave.open(output_file, "w") as wav_file:
        audio = voice.synthesize(content, wav_file)

        final_audio = AudioSegment.from_file(BytesIO(audio))
        play(final_audio)

        if args.verbose:
            print("Audio played successfully.")