from .models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
import rest_framework.status as status
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.template.loader import render_to_string
import uuid
from django.middleware import csrf
from django.http import HttpResponseRedirect
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from .authenticate import login_required


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
    email_object.delete()
    user_object.save()
    return HttpResponseRedirect("http://127.0.0.1:3000/login/")


@api_view(['POST'])
def login(request):
    data = request.data
    response = Response()        
    email = data.get('email', None)
    password = data.get('password', None)
    user = CustomUser.objects.get(email=email)
    if not user.verified:
        return JsonResponse({"Invalid" : "Please Verify your email"},status=status.HTTP_401_UNAUTHORIZED)
    password_check = user.check_password(password)
    if password_check:
        data = Token.objects.get_or_create(user=user)
        response = JsonResponse({"Success" : "Login successfully"}) 
        response.set_cookie('token',data[0])
        csrf.get_token(request)
        return response
    else:
        return JsonResponse({"Invalid" : "Invalid username or password!!"},status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
def forget_password(request):
    email = request.data['email']
    user = CustomUser.objects.get(email=email)
    UID =  uuid.uuid4()
    email_object = EmailsHandler(user=user,pass_verf=UID)
    email_object.save() 
    msg_plain = render_to_string('users/email.txt')
    msg_html = render_to_string('users/email.html', context={'verify_link':f'http://127.0.0.1:8000/users/password-reset/{UID}'})

    send_mail(
        'Password Reset Email',
        msg_plain,
        'VidBug',
        [email],
        html_message=msg_html,
    )
    return JsonResponse({'message':"Email Sent","success":True})

@api_view(['POST'])
@login_required
def reset_password(request):
    data = request.data
    user = request.user
    password = make_password(salt=user.email,password=data['password'])
    user.password = password
    user.save()
    return JsonResponse({'success':True})

@api_view(['POST','GET'])
def set_forget_password(request):
    data = request.data
    pass_object = EmailsHandler.objects.get(pass_verf=data['uuid'])
    user = CustomUser.objects.get(email=pass_object.user)
    password = make_password(salt=user.email,password=data['password'])
    user.password = password
    pass_object.delete()
    user.save()
    return JsonResponse({'success':True})    
