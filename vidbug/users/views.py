from .models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
import rest_framework.status as status
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.template.loader import render_to_string
import uuid
from rest_framework_simplejwt.tokens import RefreshToken
from django.middleware import csrf
from django.conf import settings
from django.http import HttpResponseRedirect

# Create your views here.

@api_view(['POST','GET'])
def register(request):
    data = request.data
    email = data['email']
    first_name = data['first_name']
    last_name = data['last_name']
    password = make_password(salt=email,password=data['password'])
    user = CustomUser()
    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    user.password = password
    user.save()

    UID =  uuid.uuid4()
    email_object = EmailsHandler(user=user,email_verf=UID)
    email_object.save() 
    msg_plain = render_to_string('users/email.txt')
    msg_html = render_to_string('users/email.html', context={'verify_link':f'http://127.0.0.1:8000/users/verify-email/{UID}'})

    send_mail(
        'Confirm Email',
        msg_plain,
        'VidBug',
        [email],
        html_message=msg_html,
    )

    return Response(status=status.HTTP_200_OK)

@api_view(['POST','GET'])
def verify_email(request, uuid):
    email_object = EmailsHandler.objects.get(email_verf=uuid)
    user_object = CustomUser.objects.get(email=email_object.user)
    user_object.verified = True
    user_object.save()
    return HttpResponseRedirect("http://127.0.0.1:3000/login/")


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
        
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@api_view(['POST'])
def login(request):
    data = request.data
    response = Response()        
    email = data.get('email', None)
    password = data.get('password', None)
    user = CustomUser.objects.get(email=email)
    password_check = user.check_password(password)
    if password_check:
        data = get_tokens_for_user(user)
        response.set_cookie(
                            key = settings.SIMPLE_JWT['AUTH_COOKIE'], 
                            value = data["access"],
                            expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                            secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                            httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                            samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                                )
        csrf.get_token(request)
        response.data = {"Success" : "Login successfully","data":data}
        return response
    else:
        return Response({"Invalid" : "Invalid username or password!!"},status=status.HTTP_404_NOT_FOUND)