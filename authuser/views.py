from django.shortcuts import render, redirect

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import User
from .serializers import UserSerializer, UserRegistrationSerializer
from rest_framework import viewsets
from . import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from .serializers import UserLoginSerializer
from rest_framework import status
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from rest_framework.authtoken.models import Token


class USERViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

class UserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user=serializer.save()
            token = default_token_generator.make_token(user)
            print("token ", token)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            print("uid ", uid)
            confirm_link = f"http://127.0.0.1:8000/user/active/{uid}/{token}"
            
            email_subject = "Active your Account"
            email_body = render_to_string('confirm_email.html', {'confirm_link' : confirm_link})
            
            email = EmailMultiAlternatives(email_subject , '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            return Response({'success':"Check your mail for confirmation"})

        return Response(serializer.errors)
        
def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
        print(user.id)
        print(user.pk)
    except(User.DoesNotExist):
        user = None 
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('http://127.0.0.1:5500/login.html')
    else:
        return redirect('register')
    

# class UserLoginApiView(APIView):
#     def post(self, request):
#         serializer = UserLoginSerializer(data=request.data, context={'request': request})
#         if serializer.is_valid():
#             user = serializer.validated_data['user']
#             login(request, user)
#             messages.success(request, "succesfully Register")
#             return redirect('http://127.0.0.1:8000/user/list/')
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginApiView(APIView):
    def post(self, request):
        serializer = serializers.UserLoginSerializer(data = self.request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(email= email, password=password)
            
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                print(token)
                print(_)
                login(request, user)
                print(user.id)

                return Response({'token' : token.key, 'user_id' : user.id})
            else:
                return Response({'error' : "Invalid Credential"})
        return Response(serializer.errors) 