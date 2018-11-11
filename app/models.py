from django.db import models

# Create your models here.

from django.db import models


class Respondent(models.Model):
    email = models.CharField(max_length=200)
    group = models.CharField(max_length=200)
    age = models.IntegerField(default=0)
    location = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    gender = models.CharField(max_length=200)
    level = models.IntegerField(default=0)
    enrollment_date = models.DateTimeField()
    last_update = models.DateTimeField(auto_now_add=True, blank=True)


class Panas(models.Model):
    respondent = models.ForeignKey(Respondent, on_delete=models.CASCADE)
    pre_post = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)
