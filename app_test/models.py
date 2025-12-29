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


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=255)
    answered_at = models.DateTimeField(auto_now_add=True)
    is_correct = models.BooleanField()
    

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    score = models.IntegerField(default=0)
    time_taken = models.DurationField(null=True, blank=True)
    packet = models.IntegerField()
    # last_answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    # Можно добавить поле для текущего вопроса, итд

    def __str__(self):
        return f'{self.user} - {self.score} ({self.time_taken}s)'