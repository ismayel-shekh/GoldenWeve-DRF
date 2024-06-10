from django.db import models
from authuser.models import User
# Create your models here.

class Deposit(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    deposit = models.IntegerField()