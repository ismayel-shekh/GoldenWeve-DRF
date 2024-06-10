from rest_framework import serializers
from . import models
class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Deposit
        fields = '__all__'