from rest_framework import viewsets, status
from rest_framework.response import Response
from . import models
from . import serializers
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from authuser.models import User


class DepositViewset(viewsets.ModelViewSet):
    queryset = models.Deposit.objects.all()
    serializer_class = serializers.DepositSerializer

    def create(self, request, *args, **kwargs):
        deposit = int(request.data.get('deposit'))
        user_id = int(request.data.get('User'))
        current_user = User.objects.get(id=user_id)
        print(current_user)
        print(current_user.first_name)
        if deposit >= 0:
            current_user.balance += deposit
            current_user.save()
            email_subject = "Deposit successful"
            email_body = render_to_string(
                'deposit.html', {'user': current_user, 'balance': current_user.balance, 'money': deposit})
            email = EmailMultiAlternatives(
                email_subject, '', to=[current_user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()

            return Response({"message": "Deposit successful. Check email"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Deposit amount must be positive"}, status=status.HTTP_400_BAD_REQUEST)