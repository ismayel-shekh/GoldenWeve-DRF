from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required = True)
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'mobile_number', 'password', 'confirm_password', ]

    def save(self):
        email = self.validated_data['email']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        mobile_number = self.validated_data.get('mobile_number')
        password = self.validated_data['password']
        password2 = self.validated_data['confirm_password']
        
        if password != password2:
            raise serializers.ValidationError({'error': "password Doesn't matched"})
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': "Email Already exists"})
        
        account = User( email=email, first_name = first_name, last_name = last_name, mobile_number=mobile_number)
        account.set_password(password)
        account.save()
        return account

# class UserLoginSerializer(serializers.Serializer):
#     email = serializers.EmailField(required=True)
#     password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

#     def validate(self, data):
#         email = data.get('email')
#         password = data.get('password')

#         if email and password:
#             user = authenticate(request=self.context.get('request'), email=email, password=password)
#             if not user:
#                 raise serializers.ValidationError("Invalid login credentials")
#         else:
#             raise serializers.ValidationError("Must include 'email' and 'password'")

#         data['user'] = user
#         return data

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required = True)   


class ChangePasswordSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    old_password = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        user_id = attrs.get("user_id")
        old_password = attrs.get("old_password")
        password = attrs.get("password")
        password2 = attrs.get("password2")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise ValidationError("User not found")

        if not user.check_password(old_password):
            raise ValidationError("Old password is not correct")

        if password != password2:
            raise ValidationError("New password fields didn't match")

        return attrs

    def save(self):
        user_id = self.validated_data["user_id"]
        password = self.validated_data["password"]

        user = User.objects.get(id=user_id)
        user.set_password(password)
        user.save()