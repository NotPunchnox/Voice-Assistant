import argparse
from src.listen import *
import src.ollama as ollama


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

        # Appel à l'API Ollama pour générer la réponse et activer le tts en temps réel
        responseAI = ollama.Generate(text, options={ "model": model })
