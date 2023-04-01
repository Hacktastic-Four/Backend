from django.shortcuts import render
from .models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
import rest_framework.status as status
# Create your views here.
from users.authenticate import login_required
import uuid
from django.http import JsonResponse


@api_view(['POST','GET'])
@login_required
def add_question(request):
    data = request.data
    question = data['question']
    topic = data['topic']
    UID =  uuid.uuid4()
    question_object = Question()
    question_object.user = request.user
    question_object.question = question
    question_object.topic = topic
    question_object.room_id = UID
    question_object.save()
    return JsonResponse({"success":True})

@api_view(['POST','GET'])
def get_room_id(request):
    data = request.data
    try:
        question = Question.objects.get(id=data['id'])
        return JsonResponse({'room_id':question.room_id})
    except:
        return JsonResponse({'error': "Invalid question id"})
