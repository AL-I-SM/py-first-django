from django.db import models
from classbook.models import User

class Question(models.Model):
    text = models.TextField()
    # Варианты ответов, например, через отдельную модель или JSONField
    options = models.JSONField()
    correct_option = models.CharField(max_length=255)


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=255)
    answered_at = models.DateTimeField(auto_now_add=True)
    is_correct = models.BooleanField()


class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    time_taken = models.DurationField(null=True, blank=True)
    # Можно добавить поле для текущего вопроса, итд

    def __str__(self):
        return f'{self.user} - {self.score} ({self.time_taken}s)'