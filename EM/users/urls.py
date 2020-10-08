
from django.urls import path
from .views import *

urlpatterns =[
    path('signup', signup_view, name='signup'),
    path('email_verification/<uidb4>/<token>', email_verification, name='email_verification'),
    path('login', login, name='login'),
    path('password_reset_request', password_reset_request, name='password_reset_request'),
    path('password_reset_token_check/<uidb4>/<token>', password_reset_token_check, name='password_reset_token_check'),
    path('set_new_password', set_new_password, name='set_new_password'),
    path('logout', logout, name='logout'),
]


