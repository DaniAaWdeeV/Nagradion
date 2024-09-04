from django.db import models
from django.utils import timezone
from django.contrib import admin

import datetime
# Create your models here.

class Question(models.Model):
    question_text = models.TextField(max_length=100)
    pub_date = models.DateTimeField()

    def __str__(self):
        return self.question_text

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self):
        now = timezone.now()
        return (now - datetime.timedelta(days=1)) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    vote = models.IntegerField()
    choice_text = models.CharField(max_length=100)

    def __str__(self):
        return self.choice_text
