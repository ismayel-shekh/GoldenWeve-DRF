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
from rest_framework import filters
class filterproductbuy(filters.BaseFilterBackend):
    def filter_queryset(self, request, query_set, view):
        user_id = request.query_params.get("user_id")
        if user_id == 'null':
            return query_set.none()
        if user_id:
            return query_set.filter(user = user_id)
        return query_set

class buyproductViewSet(viewsets.ModelViewSet):
    queryset = models.productbuy.objects.all()
    serializer_class = serializers.buyproductSreializer
    filter_backends = [filterproductbuy]

    def create(self, request, *args, **kwargs):

        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        customer_id = request.data.get('user')
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
                    user = current_user,
                    product = product,
                    quantiry = quantiry,
                )
            x.save()

            return Response({"message": "Buying successful"}, status=status.HTTP_201_CREATED)
        else:
                return Response({"error": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)
