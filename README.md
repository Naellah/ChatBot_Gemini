# ChatBot Gemini

Ce projet est un chatbot simple basé sur l'API Gemini de Google, composé d'un frontend en HTML/CSS/JavaScript et d'un backend en Python Flask.

## Fonctionnalités

* **Interface utilisateur interactive :** Discutez avec le modèle Gemini directement depuis votre navigateur.
* **Backend Flask :** Gère la communication sécurisée avec l'API Gemini.
* **Historique des conversations :** (Optionnel) Persistance de l'historique via Firebase (si configuré).

## Démarrage rapide

1.  **Backend (Python Flask) :**
    * Installez les dépendances : `pip install -r requirements.txt`
    * Configurez votre `GEMINI_API_KEY` (dans vos variables d'environnement ou directement dans `backend_app.py`).
    * Démarrez le serveur Flask : `python backend_app.py`

2.  **Frontend (HTML/JS) :**
    * Ouvrez un **nouveau terminal** dans le dossier de votre projet.
    * Démarrez un serveur HTTP simple : `python -m http.server 8000`
    * Accédez au chatbot dans votre navigateur : `http://127.0.0.1:8000/index.html`

---