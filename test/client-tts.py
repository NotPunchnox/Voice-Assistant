# Copyright (c) 2025 Punchnox
# https://github.com/notpunchnox
# LICENSE MIT

import requests
import os
from pydub import AudioSegment
from pydub.playback import play

# Installer pydub avec : pip install pydub
# (et ffmpeg pour lire les fichiers audio)

url = "http://127.0.0.1:5000/synthesize"

while True:

    data = {"text": input("Vous: ")}

    response = requests.post(url, json=data)

    if response.status_code == 200:
        # Sauvegarder temporairement le fichier audio
        temp_file = "temp_output.wav"
        with open(temp_file, "wb") as f:
            f.write(response.content)
        
        # Lire l'audio
        audio = AudioSegment.from_file(temp_file)
        play(audio)
        
        # Supprimer le fichier temporaire
        os.remove(temp_file)
        print("Audio lu et supprimé avec succès.")
    else:
        print("Erreur :", response.json())