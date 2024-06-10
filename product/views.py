from django.shortcuts import render
from rest_framework import viewsets
from . import models
from . import serializers
# Create your views here.
class productViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.productSreializer


from django.shortcuts import render
from rest_framework import viewsets
from . import models
from . import serializers
from rest_framework import viewsets, status
from rest_framework.response import Response
from . import models
from . import serializers
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from authuser.models import User


class buyproductViewSet(viewsets.ModelViewSet):
    queryset = models.productbuy.objects.all()
    serializer_class = serializers.buyproductSreializer


    def create(self, request, *args, **kwargs):

        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        customer_id = request.data.get('User')
        product_id = request.data.get('product')
        quantiry = int(request.data.get('quantiry'))
        current_user = User.objects.get(id=customer_id)
        print("line53",current_user.email)


        print(product_id)
        product = models.Product.objects.get(id=product_id)

        total_cost = product.price * quantiry

        if current_user.balance >= total_cost:
                # serializer.save()
            current_user.balance -= total_cost
            current_user.save()

            x = models.productbuy.objects.create(
                    User = current_user,
                    product = product,
                    quantiry = quantiry,
                )
            x.save()

            return Response({"message": "Buying successful"}, status=status.HTTP_201_CREATED)
        else:
                return Response({"error": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)
