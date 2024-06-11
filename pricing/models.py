from django.db import models
from authuser.models import User
# Create your models here.
CHOICES=[
    ('Basic', 'Basic'),
    ('Standard', 'Standard'),
    ('Premium', 'Premium'),
]
class Plan(models.Model):
    type = models.CharField(max_length=250)
    cost = models.IntegerField()
    def __str__(self):
        return self.type

class planfeaters(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    featers = models.CharField(max_length=260)
    def __str__(self):
        return self.Plan.type


class bookingplans(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    count = models.IntegerField(default=3)

    def __str__(self):
        return self.Plan.type