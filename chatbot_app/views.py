from django.shortcuts import render
from django.http import JsonResponse
from .models import QuestionAnswer, InteractionLog
from django.views.decorators.csrf import csrf_exempt
import re
import logging
import unicodedata
import json
from datetime import datetime, timedelta
import spacy
from django.views.decorators.http import require_http_methods

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Chargement du modèle spaCy
try:
    nlp = spacy.load("fr_core_news_md")
except OSError:
    spacy.cli.download("fr_core_news_md")
    nlp = spacy.load("fr_core_news_md")

# Fonctions existantes (home, products, etc.) inchangées
def home(request):
    return render(request, 'home.html')

def products(request):
    return render(request, 'products.html')

def custom(request):
    return render(request, 'custom.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def shop(request):
    return render(request, 'shop.html')

def services(request):
    return render(request, 'services.html')

def placeholder(request):
    return render(request, 'placeholder.html')

@csrf_exempt
@require_http_methods(["POST"])
def chatbot(request):
    try:
        logger.info(f"Données brutes reçues: {request.body}")
        
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError as e:
                logger.error(f"Erreur de décodage JSON: {str(e)}")
                return JsonResponse({
                    'response': 'Format de données invalide.',
                    'link': None
                })
        else:
            data = request.POST
        
        question = data.get('question', '').strip()
        logger.info(f"Question reçue: {question}")
        
        if not question:
            return JsonResponse({
                'response': 'Je ne peux pas répondre à une question vide.',
                'link': None
            })
        
        if len(question) < 3:
            return JsonResponse({
                'response': 'Votre question est trop courte. Pouvez-vous la reformuler ?',
                'link': None
            })
        
        # Nettoyage et normalisation
        question = normalize_text(question)
        question_doc = nlp(question)
        
        # Détection des entités et intentions
        entities = []
        intents = []
        question_words = {token.lemma_.lower() for token in question_doc}
        
        # Mots-clés pour les entités (sports)
        entity_keywords = {
            'football': {'foot', 'football', 'soccer'},
            'basketball': {'basket', 'basketball', 'basket-ball'},
            'volleyball': {'volley', 'volleyball', 'volley-ball'},
            'rugby': {'rugby'},
            'tennis': {'tennis'},
            'golf': {'golf'},
            'handball': {'handball', 'hand'}
        }
        
        # Mots-clés pour les intentions
        intent_keywords = {
            'prix': {'prix', 'coût', 'couût', 'coût', 'coute', 'coûte', 'tarif', 'combien', 'euro', 'mga'},
            'type': {'type', 'types', 'fabrique', 'produit', 'ballon', 'ballons'},
            'livraison': {'livraison', 'livrer', 'délai', 'delai', 'expédition', 'expedition'},
            'contact': {'contact', 'contacter', 'email', 'téléphone', 'telephone'},
            'personnalisation': {'personnalisation', 'personnaliser', 'custom', 'logo'}
        }
        
        # Détection des entités
        for entity, keywords in entity_keywords.items():
            if question_words.intersection(keywords):
                entities.append(entity)
        
        # Détection des intentions
        for intent, keywords in intent_keywords.items():
            if question_words.intersection(keywords):
                intents.append(intent)
        
        logger.info(f"Entités détectées: {entities}")
        logger.info(f"Intentions détectées: {intents}")
        
        # Récupération des questions de la base
        all_questions = QuestionAnswer.objects.all()
        
        best_match = None
        best_score = 0.0
        best_question = None
        
        # Analyse sémantique
        for qa in all_questions:
            db_question = normalize_text(qa.question)
            db_doc = nlp(db_question)
            similarity = question_doc.similarity(db_doc)
            
            # Bonus pour entités et intentions
            entity_bonus = 0.0
            intent_bonus = 0.0
            db_words = {token.lemma_.lower() for token in db_doc}
            
            # Bonus pour entités correspondantes
            if entities:
                for entity in entities:
                    if entity in qa.category.lower():
                        entity_bonus += 0.5  # Gros bonus si la catégorie correspond
                    if entity_keywords[entity].intersection(db_words):
                        entity_bonus += 0.2
                
                # Si entité détectée mais catégorie non spécifique, réduire le score
                if 'général' in qa.category.lower() and entities:
                    entity_bonus -= 0.3
            
            # Bonus pour intentions correspondantes
            if intents:
                for intent in intents:
                    if intent in qa.category.lower():
                        intent_bonus += 0.3
                    if intent_keywords[intent].intersection(db_words):
                        intent_bonus += 0.1
            
            final_score = similarity + entity_bonus + intent_bonus
            
            logger.info(f"Question: {question}")
            logger.info(f"Comparaison avec: {qa.question}")
            logger.info(f"Similarité: {similarity:.4f}")
            logger.info(f"Bonus entités: {entity_bonus:.4f}")
            logger.info(f"Bonus intentions: {intent_bonus:.4f}")
            logger.info(f"Score final: {final_score:.4f}")
            
            if final_score > best_score:
                best_score = final_score
                best_match = qa
                best_question = qa.question
        
        # Seuil de similarité
        if best_score >= 0.5:  # Seuil relevé pour plus de précision
            InteractionLog.objects.create(
                question=question,
                response=best_match.response,
                similarity_score=best_score
            )
            return JsonResponse({
                'response': best_match.response,
                'link': best_match.link
            })
        else:
            InteractionLog.objects.create(
                question=question,
                response="Je ne peux pas répondre précisément. Consultez notre catalogue ou contactez-nous.",
                similarity_score=best_score
            )
            return JsonResponse({
                'response': "Je ne peux pas répondre précisément à cette question. Consultez notre catalogue ou contactez notre service client.",
                'link': '/products'
            })
            
    except Exception as e:
        logger.error(f"Erreur dans le chatbot: {str(e)}")
        return JsonResponse({
            'response': "Désolé, une erreur s'est produite. Veuillez réessayer.",
            'link': None
        })

def normalize_text(text):
    text = unicodedata.normalize('NFD', text)
    text = ''.join([c for c in text if not unicodedata.combining(c)])
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    stop_words = {'le', 'la', 'les', 'un', 'une', 'des', 'de', 'du', 'et', 'est', 'sont', 'qui', 'que', 'quoi', 'quel', 'quelle'}
    words = text.split()
    words = [w for w in words if w not in stop_words]
    return ' '.join(words)