# Copyright (c) 2025 Punchnox
# https://github.com/notpunchnox
# LICENSE MIT

# Improtation des librairies
import requests
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play

# Fonction pour lancer le text to speech
def sendTTS(content, args):
    response = requests.post("http://127.0.0.1:5000/synthesize", json={"text": content})

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