from django.test import TestCase, Client
from django.urls import reverse
import json

class ChatbotTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Création des questions de test
        self.test_questions = [
            {
                "question": "Quel est le prix de vos ballons ?",
                "response": "Nos ballons sont disponibles à partir de 50000 MGA l'unité. Le prix varie selon le type et la quantité.",
                "category": "prix",
                "link": "/prix"
            },
            {
                "question": "Combien de temps pour la livraison ?",
                "response": "La livraison standard prend 2-3 jours ouvrés. La livraison express est disponible en 24h.",
                "category": "livraison",
                "link": "/livraison"
            },
            {
                "question": "Quelle est la garantie de qualité ?",
                "response": "Tous nos ballons sont garantis 1 an contre les défauts de fabrication.",
                "category": "qualite",
                "link": "/garantie"
            }
        ]
        
        # Création des questions dans la base de données
        for q in self.test_questions:
            self.client.post(reverse('admin:chatbot_app_questionanswer_add'), q)

    def test_similar_questions(self):
        """Test des questions similaires"""
        similar_questions = [
            ("Quel est le prix de vos ballons ?", "Combien coûtent vos ballons ?"),
            ("Quelle est la garantie de qualité ?", "Quelle est la garantie de qualite ?"),
            ("Combien de temps pour la livraison ?", "Quel est le délai de livraison ?")
        ]
        
        for q1, q2 in similar_questions:
            response1 = self.client.post(
                reverse('chatbot'),
                json.dumps({'question': q1}),
                content_type='application/json'
            )
            response2 = self.client.post(
                reverse('chatbot'),
                json.dumps({'question': q2}),
                content_type='application/json'
            )
            
            self.assertEqual(
                response1.json()['response'],
                response2.json()['response'],
                f"Les questions '{q1}' et '{q2}' devraient avoir la même réponse"
            )

    def test_empty_question(self):
        """Test d'une question vide"""
        response = self.client.post(
            reverse('chatbot'),
            json.dumps({'question': ''}),
            content_type='application/json'
        )
        self.assertEqual(
            response.json()['response'],
            'Je ne peux pas répondre à une question vide.'
        )

    def test_short_question(self):
        """Test d'une question trop courte"""
        response = self.client.post(
            reverse('chatbot'),
            json.dumps({'question': 'a'}),
            content_type='application/json'
        )
        self.assertEqual(
            response.json()['response'],
            'Votre question est trop courte. Pouvez-vous la reformuler ?'
        )

    def test_complex_question(self):
        """Test d'une question complexe"""
        response = self.client.post(
            reverse('chatbot'),
            json.dumps({
                'question': 'Je souhaite commander des ballons pour un événement, pouvez-vous me dire les prix et les délais de livraison ?'
            }),
            content_type='application/json'
        )
        self.assertIn('prix', response.json()['response'].lower())
        self.assertIn('livraison', response.json()['response'].lower())
