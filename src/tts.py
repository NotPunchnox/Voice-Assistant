# Copyright (c) 2025 Punchnox
# https://github.com/notpunchnox
# LICENSE MIT

# Improtation des librairies
import requests
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play

from piper.voice import PiperVoice
import wave
import os

# Charger le modèle Piper
model = "./ressources/voice/fr_FR-tom-medium.onnx"
voice = PiperVoice.load(model)

# Fonction pour lancer la synthèse vocale
def sendTTS(content, args):
    output_file = "output.wav"
    with wave.open(output_file, "w") as wav_file:
        audio = voice.synthesize(text, wav_file)

    if args.verbose:
        print(f"Sending request to TTS API with text: {content}") 

    if response.status_code == 200:
        audio = AudioSegment.from_file(BytesIO(response.content))
        play(audio)

        # Lecture de l'audio
        if args.verbose:
            print("Audio played successfully.")
    else:
        print(f"Error: {response.status_code} - {response.json()}")