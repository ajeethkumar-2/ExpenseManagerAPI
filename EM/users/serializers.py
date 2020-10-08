from django.utils.encoding import force_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.exceptions import AuthenticationFailed
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from django.contrib import auth
from .models import User


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    password_confirm = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'password_confirm']

    def save(self, **kwargs):
        user = User(
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name']
        )
        password = self.validated_data['password']
        password_confirm = self.validated_data['password_confirm']

        if not password == password_confirm:
            raise serializers.ValidationError({'Message': 'Password does not match'})
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, Please try again..!!')

        if not user.is_active:
            raise AuthenticationFailed('Account Disabled, Please contact Admin..!!')

        if not user.is_verified:
            raise AuthenticationFailed('Account is not verified, Please click the link sent to '
                                       'your email to activate the account..!!')

        return user


class PasswordResetSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['email']


class PasswordResetTokenCheckSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=255, write_only=True)
    uidb4 = serializers.CharField(max_length=58, write_only=True)

    class Meta:
        model = User
        fields = ['token', 'uidb4']

    def validate(self, attrs):
        try:
            token = attrs.get('token')
            uidb4 = attrs.get('uidb4')
        except Exception as error:
            raise AuthenticationFailed({'error': error})



class SetNewPasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(max_length=58, min_length=6, write_only=True)
    token = serializers.CharField(max_length=255, write_only=True)
    uidb4 = serializers.CharField(max_length=58, write_only=True)

    class Meta:
        model = User
        fields = ['new_password', 'token', 'uidb4']

    def validate(self, attrs):
        try:
            new_password = attrs.get('new_password')
            token = attrs.get('token')
            uidb4 = attrs.get('uidb4')
            id = force_str(urlsafe_base64_decode(uidb4))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid')
            user.set_password(new_password)
            user.save()
            return user
        except Exception as error:
            raise AuthenticationFailed({'error': error})
        return super().validate(attrs)

