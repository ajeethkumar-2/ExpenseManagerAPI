from .serializers import *
from django.utils.encoding import DjangoUnicodeDecodeError, force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.urls import reverse
from .models import User
from .utils import Util


@api_view(['POST'])
def signup_view(request):
    if request.method == 'POST':
        serializer = SignUpSerializer(data=request.data)
        email = request.data['email']
        first_name = request.data['first_name']
        if serializer.is_valid():
            serializer.save()
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                uidb4 = urlsafe_base64_encode(force_bytes(user.id))
                token = PasswordResetTokenGenerator().make_token(user)
                current_site = get_current_site(request=request).domain
                relativeLink = reverse('email_verification', kwargs={'uidb4': uidb4, 'token': token})
                absolute_url = 'http://' + current_site + relativeLink
                email_body = 'Hello, ' + first_name + '\n\nUse the link verify your email id ' \
                                                      'and to complete the registration\n\n' + absolute_url
                data = {'email_subject': 'Verify your email id', 'email_body': email_body, 'to_email': user.email}
                Util.send_email(data)

                return Response({
                    'message': 'New user created SuccessFully. '
                               'Check your mail and verify your email id to complete the registration',
                    'data': serializer.data,
                    'uidb4': uidb4,
                    'token': token,

                }, status=status.HTTP_201_CREATED)

        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def email_verification(request, uidb4, token):
    serializer = PasswordResetTokenCheckSerializer
    print(uidb4)
    print(token)
    if request.method == 'GET':
        try:
            id = urlsafe_base64_decode(uidb4)
            user = User.objects.get(id=id)
            verification = PasswordResetTokenGenerator()
            if verification.check_token(user, token):
                user.is_verified = True
                user.save()
                return Response({'message': 'Congratulations, Your email id had verified, You can login Now.'},
                                status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Verification - Token is not valid, Please request a new one'},
                                status=status.HTTP_401_UNAUTHORIZED)

        except DjangoUnicodeDecodeError:
            return Response({'error': 'Token is not valid, Please request a new one'},

                            status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        email = request.data['email']
        user = User.objects.get(email=email)
        serializer.is_valid(raise_exception=True)
        if User.objects.filter(email=email).exists() and user.is_verified is True:
            token = Token.objects.get_or_create(user=user)
            return Response({'message': 'Login Successful.', 'token': str(token[0])})
        else:
            return Response({'message': 'Please verify your email and then try to login.'})
    return Response({'error': 'No user registered with this email'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def password_reset_request(request):
    if request.method == 'POST':
        serializer = PasswordResetSerializer(data=request.data)
        email = request.data['email']
        if serializer.is_valid():
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                uidb4 = urlsafe_base64_encode(force_bytes(user.id))
                token = PasswordResetTokenGenerator().make_token(user)
                current_site = get_current_site(request=request).domain
                relativeLink = reverse('password_reset_token_check', kwargs={'uidb4': uidb4, 'token': token})
                absolute_url = 'http://' + current_site + relativeLink
                email_body = 'Hello, \n Use the link below to reset your password. \n' + absolute_url
                data = {'email_subject': 'Reset your Password', 'email_body': email_body, 'to_email': user.email}
                Util.send_email(data)
                id = urlsafe_base64_decode(force_str(uidb4))
                return Response(
                    {'message': 'We have sent you the link to reset your password..!!', 'id': id, 'user': user.id,
                     'uidb4': uidb4, 'token': token}, status=status.HTTP_200_OK)

        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def password_reset_token_check(request, uidb4, token):
    if request.method == 'GET':
        try:
            id = (force_str(urlsafe_base64_decode(uidb4)))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is Invalid, Request new one'},
                                status=status.HTTP_401_UNAUTHORIZED)

            return Response({'message': 'Credentials is Valid', 'uidb4': uidb4, 'token': token},
                            status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError:
            return Response({'error': 'Token is Invalid, Request new one'},
                            status=status.HTTP_401_UNAUTHORIZED)


@api_view(['PUT'])
def set_new_password(request):
    if request.method == 'PUT':
        serializer = SetNewPasswordSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'message': 'Password Reset Success..!!'}, status=status.HTTP_200_OK)

        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def logout(request):
    if request.method == 'GET':
        request.user.auth_token.delete()
        return Response({'message': 'Logged Out Successfully.'}, status=status.HTTP_200_OK)
