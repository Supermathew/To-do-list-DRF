from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login

Account = get_user_model()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        try:
            user = Account.objects.get(email=email)
        except Account.DoesNotExist:
            raise serializers.ValidationError('Account with This email does not Exist please create one')

        if not user.is_active:
            raise serializers.ValidationError('User account is inactive. Please verify your email.')

        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError('Invalid login credentials')


        return {
            'email': user.email,
            'user':user,
        } 

    def create(self, validated_data):
        user = authenticate(
            email=validated_data['email'],
            password=validated_data['password']
        )
        update_last_login(None, user)
        return user
      