# Copyright (c) 2025 Punchnox
# https://github.com/notpunchnox
# LICENSE MIT

# Importation des librairies internes et externes
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
        # Si l'utilisateur est en version CLI alors lui demander son prompt
        text = input("Enter your text: ")
    else:
        # Ecoute de l'utilisateur
        text = process_audio()

    # Si le text est reconnue alors l'afficher et continuer le programme
    if text:
        print(f"\nQuestion reconnue: {text}")

        # Appel au module local ollama
        responseAI = ollama.Generate(text, args, options={ "model": model })