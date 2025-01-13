# Copyright (c) 2025 Punchnox
# https://github.com/notpunchnox
# LICENSE MIT




def synthesize(text):
    try:
        # Générer un fichier audio temporaire
        
        
        # Envoyer le fichier audio au client
        response = send_file(output_file, as_attachment=False)
        
        # Supprimer le fichier après l'envoi
        os.remove(output_file)
        
        return response
    
    except Exception as e:
        print("Error:", e)