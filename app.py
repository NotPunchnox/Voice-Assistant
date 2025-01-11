import argparse
import requests
from pydub import AudioSegment
from pydub.playback import play
from src.listen import *
import src.ollama as ollama
from io import BytesIO

# Argument parser pour gérer les paramètres en ligne de commande
parser = argparse.ArgumentParser(description="Interactive AI model with voice recognition and TTS.")
parser.add_argument('--cli', action='store_true', help="Activate CLI mode (no voice input).")
parser.add_argument('--verbose', action='store_true', help="Enable verbose output.")
parser.add_argument('--model', type=str, default="qwen2.5:3b", help="Specify the AI model to use.")
args = parser.parse_args()

text = ""
model = args.model

# Boucle principale
while True:
    if args.cli:
        text = input("Enter your text: ")
    else:
        text = process_audio()

    if text:
        print(f"\nQuestion reconnue: {text}")

        # Appel à l'API Ollama pour générer la réponse
        responseAI = ollama.Generate(text, options={ "model": model })
        response = requests.post("http://127.0.0.1:5000/synthesize", json={"text": responseAI})

        if args.verbose:
            print(f"Sending request to TTS API with text: {text}") 

        if response.status_code == 200:
            # Lecture de l'audio
            audio = AudioSegment.from_file(BytesIO(response.content))
            play(audio)
            print("Audio played successfully.")
        else:
            print(f"Error: {response.status_code} - {response.json()}")

