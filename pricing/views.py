from django.shortcuts import render
from rest_framework import viewsets
from . import models
from . import serializers
from rest_framework import viewsets, status
from rest_framework.response import Response
from . import models
from .models import bookingplans
from rest_framework import filters
from . import serializers
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from authuser.models import User

class planesviewset(viewsets.ModelViewSet):
    queryset = models.Plan.objects.all()
    serializer_class = serializers.plansSerializer

class filterfeatres(filters.BaseFilterBackend):
    def filter_queryset(self, request, query_set, view):
        plan_id = request.query_params.get("plan_id")
        if plan_id == 'null':
            return query_set.none()
        if plan_id:
            return query_set.filter(plan = plan_id)
        return query_set

class plansfeatersviewset(viewsets.ModelViewSet):
    queryset = models.planfeaters.objects.all()
    serializer_class = serializers.plansfeatersSerializer
    filter_backends = [filterfeatres]

class bookingplansviewset(viewsets.ModelViewSet):
    queryset = models.bookingplans.objects.all()
    serializer_class = serializers.bookingplansSerializer

    def create(self, request, *args, **kwargs):

        customer_id = request.data.get('User')
        plans = request.data.get('Plan')
        quantiry = int(request.data.get('count'))
        quantiry += 1
        current_user = User.objects.get(id=customer_id)
        plan = models.Plan.objects.get(id=plans)

        total_cost = plan.cost



        if quantiry <= 3:
            if current_user.balance >= total_cost:
                # serializer.save()
                current_user.balance -= total_cost
                current_user.save()


                print("booking")
                x = models.bookingplans.objects.create(
                    User = current_user,
                    Plan = plan,
                    count = quantiry,
                )
                x.save()
                return Response({"message": "plans  booking succesfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "All plans book Done"}, status=status.HTTP_400_BAD_REQUEST)
