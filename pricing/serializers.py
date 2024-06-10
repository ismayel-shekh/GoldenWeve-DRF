from rest_framework import serializers
from . import models

class plansSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Plan
        fields = '__all__'
    
class plansfeatersSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.planfeaters
        fields = '__all__'

class bookingplansSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.bookingplans
        fields = '__all__'
        