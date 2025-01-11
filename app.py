from src.listen import *

import requests
import os
from pydub import AudioSegment
from pydub.playback import play

text = ""

# Boucle principale
while True:

    # Traiter l'entrée vocale
    text = process_audio()

    # Si du texte a été reconnu
    if text:
        print(f"\nQuestion reconnue: {text}")

        response = requests.post("http://127.0.0.1:5000/synthesize", json={"text": text})

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