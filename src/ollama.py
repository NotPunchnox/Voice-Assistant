import requests

def Generate(prompt, options):
    # Si l'url de l'api n'est pas spécifié alors mettre l'url par défaut
    url = options.get("url", "http://127.0.0.1:11434/api/")

    # Préparer les données à envoyer dans la requête
    data = {
        "model": options.get("model", "qwen2.5:3b"),
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }

    try:
        # Envoi de la requête POST avec le prompt et les options
        response = requests.post(url + "chat", json=data)

        # Vérification de la réponse
        if response.status_code == 200:
            response_data = response.json()
            # Extraire le contenu de la réponse
            print(response_data)
            content = response_data.get("message", {}).get("content", "")
            
            print(content)
            return content

        else:
            print(f"Erreur {response.status_code}: {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Une erreur est survenue lors de l'appel API : {e}")
        return None

