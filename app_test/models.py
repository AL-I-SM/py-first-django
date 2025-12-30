from django.db import models
from classbook.models import User
from classbook.models import Disciplines


class Question(models.Model):
    text = models.TextField()
    number = models.IntegerField()
    # Варианты ответов, например, через отдельную модель или JSONField
    options = models.JSONField()
    correct_answer = models.CharField(max_length=255)
    packet = models.IntegerField()
    subject = models.ForeignKey(Disciplines, on_delete=models.PROTECT)
    score = models.IntegerField()


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=255)
    answered_at_client = models.DateTimeField(null=True)
    answered_at_server = models.DateTimeField(null=True)
    is_correct = models.BooleanField(null=True)
    

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    score = models.IntegerField(default=0)
    time_taken =  models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()
    packet = models.IntegerField()
    # last_answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    # Можно добавить поле для текущего вопроса, итд

    def __str__(self):
        return f'{self.user} - {self.score} ({self.time_taken}s)'