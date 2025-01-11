import pyaudio
import json
import requests
from vosk import Model, KaldiRecognizer

# Chemin du modèle français Vosk
model_path = "ressources/regonization/vosk-model-small-fr-0.22"

# Initialiser le modèle Vosk
model = Model(model_path)
recognizer = KaldiRecognizer(model, 16000)

# Fonction pour traiter l'entrée vocale
def process_audio():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4000)
    stream.start_stream()

    print("Parlez dans le micro...")
    
    silence_count = 0
    silence_threshold = 10
    final_text = ""

    try:
        while True:
            data = stream.read(4000, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                result_text = json.loads(result)["text"]
                print(result_text, end=' ', flush=True)
                final_text += result_text + " "
                silence_count = 0
            else:
                partial_result = recognizer.PartialResult()
                partial_text = json.loads(partial_result)["partial"]
                print(partial_text, end='\r', flush=True)

                if partial_text == "":
                    silence_count += 1
                else:
                    silence_count = 0

                if silence_count > silence_threshold:
                    print("\nEnregistrement terminé automatiquement.")
                    break

    except KeyboardInterrupt:
        print("\nEnregistrement interrompu par l'utilisateur.")

    # Arrêter l'enregistrement audio
    stream.stop_stream()
    stream.close()
    audio.terminate()

    return final_text.strip()