# backend_app.py
import os
from flask import Flask, request, jsonify
from flask_cors import CORS # Pour gérer les requêtes Cross-Origin
import google.generativeai as genai
# from dotenv import load_dotenv # Décommenter et installer `python-dotenv` si vous utilisez un fichier .env localement

# load_dotenv() # Décommenter si le chargement de la clé API depuis .env

app = Flask(__name__)
CORS(app) # Active CORS pour permettre les requêtes du frontend

# Configurez la clé API Gemini.
# Dans une application web déployée, il est crucial de gérer les clés API de manière sécurisée
# et d'éviter de les exposer directement dans le code côté client.
# Pour cet exemple, nous supposons que la clé API est définie comme une variable d'environnement.
# Si vous exécutez localement, assurez-vous que GEMINI_API_KEY est défini dans votre environnement.
genai.configure(api_key=os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")) # REMPLACEZ PAR VOTRE CLÉ API GEMINI

# Créez la configuration du modèle Gemini
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
)

@app.route('/chat', methods=['POST'])
def chat():
    """
    Endpoint pour gérer les requêtes de chat du frontend.
    Reçoit le message de l'utilisateur et l'historique du chat,
    puis envoie à l'API Gemini et renvoie la réponse.
    """
    data = request.get_json()
    user_message = data.get('message')
    chat_history_from_frontend = data.get('history', [])
    user_id = data.get('userId', 'anonymous') # Récupérer l'ID utilisateur du frontend

    if not user_message:
        return jsonify({"error": "Message manquant"}), 400

    print(f"[{user_id}] Message reçu : {user_message}")

    try:
        # L'historique est déjà formaté correctement par le frontend
        # et est passé directement à start_chat.
        chat_session = model.start_chat(history=chat_history_from_frontend)
        response = chat_session.send_message(user_message)

        bot_response = response.text
        print(f"[{user_id}] Réponse Gemini : {bot_response}")
        return jsonify({"response": bot_response})

    except Exception as e:
        print(f"Erreur lors de la communication avec Gemini : {e}")
        return jsonify({"error": f"Erreur interne du serveur : {e}"}), 500

if __name__ == '__main__':
    # Pour exécuter l'application Flask :
    # 1. Assurez-vous d'avoir Flask et Flask-CORS installés :
    #    pip install Flask Flask-CORS google-generativeai
    # 2. Définissez votre clé API Gemini comme variable d'environnement :
    #    export GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE" (Linux/macOS)
    #    set GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE" (Windows cmd)
    #    $env:GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE" (Windows PowerShell)
    # 3. Exécutez ce script :
    #    python backend_app.py
    # Le serveur Flask démarrera sur http://127.0.0.1:5000/
    app.run(debug=True, port=5000)
