#from django.db import models

# Create your models here.
from django.db import models

class FlashcardSet(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Flashcard(models.Model):
    set = models.ForeignKey(FlashcardSet, on_delete=models.CASCADE, related_name='cards')
    question = models.CharField(max_length=255)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

class FlashcardProgress(models.Model):
    set = models.ForeignKey(FlashcardSet, on_delete=models.CASCADE, null=True, blank=True)
    predefined_key = models.CharField(max_length=50, null=True, blank=True)
    completed = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    percentage = models.FloatField(default=0)

    def __str__(self):
        if self.set:
            return f"User set: {self.set.name}"
        return f"Predefined set: {self.predefined_key}"