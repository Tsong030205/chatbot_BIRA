from django.db import models
from django.utils import timezone

# Create your models here.
class QuestionAnswer(models.Model):
    question = models.CharField(max_length=500)
    response = models.TextField()
    category = models.CharField(max_length=100, blank=True)
    link = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.question

class InteractionLog(models.Model):
    question = models.CharField(max_length=500)
    response = models.TextField(default="Pas de réponse")
    similarity_score = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.question} - {self.created_at}"