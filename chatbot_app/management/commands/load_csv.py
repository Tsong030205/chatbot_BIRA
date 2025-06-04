import pandas as pd
from django.core.management import BaseCommand
from chatbot_app.models import QuestionAnswer

class Command(BaseCommand):
    help = 'Load data from bira_data.csv into QuestionAnswer model'

    def handle(self, *args, **kwargs):
        #Chemin vers le fichier CSV
        csv_file = 'data/data_bira.csv'
        #Lire le csv
        df = pd.read_csv(csv_file)
        #Vider la table existante
        QuestionAnswer.objects.all().delete()
        #Inserer les données dans la table
        for _, row in df.iterrows():
            QuestionAnswer.objects.create(
                question=row['Question'],
                response=row['Réponse'],
                category=row['Catégorie'],
                link=row['Lien'] if pd.notna(row['Lien']) else ''
            )
        self.stdout.write(self.style.SUCCESS('Données insérées avec succès'))