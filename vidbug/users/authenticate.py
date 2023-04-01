from rest_framework.response import Response
from rest_framework import status

from rest_framework.authtoken.models import Token
import functools

def login_required(view_func):

    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        token = request.META['HTTP_AUTHORIZATION'].split()[1]
        print(token)
        if token:
            user = Token.objects.get(key=token).user
            if user:
                request.user = user
                return view_func(request,*args, **kwargs)
            else:
                return Response({'error': 'Invalid Token'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Login Required'}, status=status.HTTP_401_UNAUTHORIZED)

    return wrapper

