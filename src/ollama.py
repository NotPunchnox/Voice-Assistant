# Copyright (c) 2025 Punchnox
# https://github.com/notpunchnox
# LICENSE MIT

import requests
import json
from .tts import sendTTS

def Generate(prompt, args, options):
    # Si l'url de l'API n'est pas spécifié alors mettre l'url par défaut
    url = options.get("url", "http://127.0.0.1:11434/api/")

    data = {
        "model": options.get("model", "qwen2.5:3b"),
        "messages": [{"role": "user", "content": prompt}],
        "stream": True
    }

    try:
        # Envoi de la requête POST avec le prompt et les options
        response = requests.post(url + "chat", json=data, stream=True)

        # Vérification de la réponse
        if response.status_code == 200:
            # Initialiser une variable pour construire progressivement le message
            content = ""
            
            # Lire chaque ligne du flux
            for chunk in response.iter_lines():
                if chunk:
                    # Décoder chaque ligne en UTF-8
                    chunk_data = chunk.decode('utf-8')
                    chunk_data = json.loads(chunk_data)["message"]["content"]
                    
                    # Ajoute le nouveau token au content
                    content += chunk_data

                    # Vérifier si une phrase complète est reçue pour le TTS
                    if content.endswith(('.', ',', ';', '!', '?')):
                        print(f"Envoi au TTS: {content}")
                        sendTTS(content, args)

                        # Réinitialiser la variable content pour préparer le prochain segment
                        content = ""
                        
            return content

        else:
            print(f"Erreur {response.status_code}: {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Une erreur est survenue lors de l'appel API : {e}")
        return None

