import os
from flask import Flask, request, jsonify
from flask_cors import CORS # Pour gérer les requêtes Cross-Origin
import google.generativeai as genai



app = Flask(__name__)
CORS(app)

genai.configure(api_key=os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")) # REMPLACEZ PAR VOTRE CLÉ API GEMINI


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
    data = request.get_json()
    user_message = data.get('message')
    chat_history_from_frontend = data.get('history', [])
    user_id = data.get('userId', 'anonymous') # Récupérer l'ID utilisateur du frontend

    if not user_message:
        return jsonify({"error": "Message manquant"}), 400

    print(f"[{user_id}] Message reçu : {user_message}")

    try:
        chat_session = model.start_chat(history=chat_history_from_frontend)
        response = chat_session.send_message(user_message)

        bot_response = response.text
        print(f"[{user_id}] Réponse Gemini : {bot_response}")
        return jsonify({"response": bot_response})

    except Exception as e:
        print(f"Erreur lors de la communication avec Gemini : {e}")
        return jsonify({"error": f"Erreur interne du serveur : {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
