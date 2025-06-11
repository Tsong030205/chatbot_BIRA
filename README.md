# BIRA Entreprise - Chatbot

Un chatbot intelligent pour BIRA Entreprise, spécialisé dans la vente de ballons de sport à Madagascar.

## Fonctionnalités

- Réponses automatiques aux questions sur les produits
- Support multilingue (Français)
- Interface utilisateur intuitive
- Intégration avec spaCy pour une meilleure compréhension des questions
- Base de données de questions/réponses extensible

## Installation

1. Cloner le repository :
```bash
git clone https://github.com/Tsong030205/chatbot_BIRA.git
cd chatbot_BIRA
```

2. Créer un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

4. Appliquer les migrations :
```bash
python manage.py migrate
```

5. Charger les données initiales :
```bash
python manage.py load_csv
```

6. Lancer le serveur :
```bash
python manage.py runserver
```

## Structure du Projet

- `chatbot_app/` : Application principale du chatbot
- `data/` : Données CSV pour les questions/réponses
- `static/` : Fichiers statiques (CSS, JS, images)
- `templates/` : Templates HTML
- `manage.py` : Script de gestion Django

## Technologies Utilisées

- Django
- spaCy
- HTML/CSS/JavaScript
- SQLite

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou à soumettre une pull request.

## Licence

Ce projet est sous licence MIT. 
