import requests
import audio
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play

def sendTTS(content, args):
    response = requests.post("http://127.0.0.1:5000/synthesize", json={"text": content})

    if args.verbose:
        print(f"Sending request to TTS API with text: {text}") 

    if response.status_code == 200:
        # Lecture de l'audio
        audio = AudioSegment.from_file(BytesIO(response.content))
        play(audio)
        print("Audio played successfully.")
    else:
        print(f"Error: {response.status_code} - {response.json()}")


def Generate(prompt, options, args):
    # Si l'url de l'API n'est pas spécifié alors mettre l'url par défaut
    url = options.get("url", "http://127.0.0.1:11434/api/")

    # Préparer les données à envoyer dans la requête
    data = {
        "model": options.get("model", "qwen2.5:3b"),
        "messages": [{"role": "user", "content": prompt}],
        "stream": True  # On active le mode stream
    }

    try:
        # Envoi de la requête POST avec le prompt et les options
        response = requests.post(url + "chat", json=data, stream=True)

        # Vérification de la réponse
        if response.status_code == 200:
            # Initialiser une variable pour construire progressivement le message
            content = ""
            
            # Itérer sur chaque partie du flux (stream)
            for chunk in response.iter_lines():
                if chunk:
                    # Décoder chaque ligne en UTF-8
                    chunk_data = chunk.decode('utf-8')
                    # Vérifier si les données reçues sont valides
                    if "message" in chunk_data:
                        # Ajouter la partie du message à content
                        content += chunk_data.split("message")[-1]
                        print(content)  # Afficher le message généré jusqu'à présent
                        
                        # Vérifier si une phrase complète est reçue pour le TTS
                        if content.endswith(('.', ',', ';', '!', '?')):
                            # Ici, tu appelles la fonction TTS pour lire le message à chaque phrase
                            print(f"Envoi au TTS: {content}")
                            # Code pour envoyer à TTS (ex: appeler une fonction de synthèse vocale ici)
                            # send_to_tts(content)  # Par exemple, send_to_tts() pour envoyer au moteur TTS

                            # Réinitialiser la variable content pour préparer le prochain segment
                            content = ""
                        
            return content

        else:
            print(f"Erreur {response.status_code}: {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Une erreur est survenue lors de l'appel API : {e}")
        return None


def Generate(prompt, options):
    # Si l'url de l'API n'est pas spécifié alors mettre l'url par défaut
    url = options.get("url", "http://127.0.0.1:11434/api/")

    data = {
        "model": options.get("model", "qwen2.5:3b"),
        "messages": [{"role": "user", "content": prompt}],
        "stream": True  # On active le mode stream
    }

    try:
        # Envoi de la requête POST avec le prompt et les options
        response = requests.post(url + "chat", json=data, stream=True)

        # Vérification de la réponse
        if response.status_code == 200:

            content = ""
            
            # Itérer sur chaque partie du flux (stream)
            for chunk in response.iter_lines():
                if chunk:
                    # Décoder chaque ligne en UTF-8
                    chunk_data = chunk.decode('utf-8')
                    if "message" in chunk_data:
                        # Ajouter la partie du message à content
                        content += chunk_data.split("message")[-1]
                        print(content)
                        
                        # Vérifier si une phrase complète est reçue pour le TTS
                        if content.endswith(('.', ',', ';', '!', '?')):
                            print(f"Envoi au TTS: {content}")
                            sendTTS(content)

                            content = ""
                        
            return content

        else:
            print(f"Erreur {response.status_code}: {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Une erreur est survenue lors de l'appel API : {e}")
        return None

