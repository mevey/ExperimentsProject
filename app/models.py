from django.db import models

# Create your models here.

from django.db import models


class Respondent(models.Model):
    email = models.CharField(max_length=200, null=True)
    group = models.CharField(max_length=200)
    age = models.IntegerField(default=0)
    education = models.CharField(max_length=200, default=None)
    location = models.CharField(max_length=200, default=None)
    pre_color = models.CharField(max_length=200, default=None)
    post_color = models.CharField(max_length=200, default=None)
    gender = models.CharField(max_length=200)
    number = models.IntegerField(default=0)
    level = models.IntegerField(default=0)
    enrollment_date = models.DateTimeField()
    time_in = models.DateTimeField(null=True)
    time_out = models.DateTimeField(null=True)
    last_update = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return str(self.id) + " (" + self.group + ")"


class Panas(models.Model):
    respondent = models.ForeignKey(Respondent, on_delete=models.CASCADE)
    pre_post = models.CharField(max_length=200)
    question = models.CharField(max_length=200, default=None)
    answer = models.CharField(max_length=200, default=None)
