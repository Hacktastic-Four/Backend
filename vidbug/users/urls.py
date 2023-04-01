from django.urls import path
from .views import *
urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('verify-email/<uuid:uuid>/', verify_email, name='verify_email'),
    path('reset-password/', reset_password, name='reset_password'),
    path('forget-password/', forget_password, name='forget_password'),
    path('set-forget-password/', set_forget_password, name='set_forget_password'),
]
