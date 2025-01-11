from flask import Flask, request, jsonify, send_file
from piper.voice import PiperVoice
import wave
import os

# Charger le modèle Piper
model = "./ressources/voice/fr_FR-tom-medium.onnx"
voice = PiperVoice.load(model)

# Créer l'application Flask
app = Flask(__name__)

# Endpoint pour la synthèse vocale
@app.route('/synthesize', methods=['POST'])
def synthesize():
    try:
        # Récupérer les données JSON envoyées dans la requête
        data = request.get_json()
        if 'text' not in data:
            return jsonify({'error': 'Le champ "text" est requis'}), 400
        
        text = data['text']
        
        # Générer un fichier audio temporaire
        output_file = "output.wav"
        with wave.open(output_file, "w") as wav_file:
            audio = voice.synthesize(text, wav_file)
        
        # Envoyer le fichier audio au client
        response = send_file(output_file, as_attachment=False)
        
        # Supprimer le fichier après l'envoi
        os.remove(output_file)
        
        return response
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Exécuter le serveur Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)