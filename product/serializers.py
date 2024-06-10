from rest_framework import serializers
from . import models

class productSreializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'

class buyproductSreializer(serializers.ModelSerializer):
    class Meta:
        model = models.productbuy
        fields = '__all__'
