from django.db import models
from django.contrib.auth.models import User


class Courses(models.Model):
    name = models.CharField()
    price = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()


class Curchased_courses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
