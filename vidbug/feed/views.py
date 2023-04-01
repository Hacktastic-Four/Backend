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
    description = data['description']
    UID =  uuid.uuid4()
    question_object = Question()
    question_object.user = request.user
    question_object.question = question
    question_object.topic = topic
    question_object.room_id = UID
    question_object.description = description
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

@api_view(['POST','GET'])
@login_required
def add_answer(request):
    user = request.user
    data = request.data
    question = Question.objects.get(id=data['id'])
    answer = Answer()
    answer.question = question
    answer.user = user
    answer.answer = data['answer']
    answer.save()
    return JsonResponse({"success":True})

@api_view(['POST','GET'])
@login_required
def upvote_answer(request):
    data = request.data
    answer = Answer.objects.get(id=data['id'])
    answer.upvote.add(request.user)
    upvote_count = answer.upvote_count()
    return JsonResponse({'success':True,'upvote_count':upvote_count})

@api_view(['POST','GET'])
@login_required
def downvote_answer(request):
    data = request.data
    answer = Answer.objects.get(id=data['id'])
    answer.downvote.add(request.user)
    downvote_count = answer.downvote_count()
    return JsonResponse({'success':True,'downvote_count':downvote_count})

@api_view(['POST','GET'])
def get_all_questions(request):
    questions = Question.objects.filter(open=True).order_by('-id')
    data = []
    for question in questions:
        temp = {
            'question': question.question,
            'user': question.user.email,
            'topic': question.topic,
            'description': question.description,
            'timestamp': question.timestamp
        }
        data.append(temp)
    return JsonResponse({'questions':data})

@api_view(['POST','GET'])
@login_required
def get_skills_questions(request):
    user = request.user
    skills = user.skills.split()
    questions = Question.objects.filter(open=True, topic__in=skills).order_by('-id')
    data = []
    for question in questions:
        temp = {
            'question': question.question,
            'user': question.user.email,
            'topic': question.topic,
            'description': question.description,
            'timestamp': question.timestamp
        }
        data.append(temp)
    return JsonResponse({'questions':data})

@api_view(['POST','GET'])
def get_detailed_question(request, id):
    question = Question.objects.get(id = id)
    data = {
        'question': question.question,
        'user': question.user.email,
        'topic': question.topic,
        'description': question.description,
        'timestamp': question.timestamp

    }
    return JsonResponse({'question':data})

@api_view(['POST','GET'])
@login_required
def get_user(request):
    print(request.user)
    data = request.data
    print(data)
    question = Question.objects.get(room_id=data['room_id'])
    if request.user != question.user:
        question.expert = request.user
    question.save()
    return JsonResponse({'status':'success'})

@api_view(['POST','GET'])
def give_rating(request):
    print(request.data)
    data = request.data
    question = Question.objects.get(room_id=data['roomId'])
    expert = question.expert
    expert.rating_count += 1
    expert.rating = (expert.rating + float(data['rating']) ) / expert.rating_count
    expert.save()
    return JsonResponse({'status':'success'})

@api_view(['POST','GET'])
@login_required
def is_author(request):
    print(request.user)
    data = request.data
    print(data)
    question = Question.objects.get(room_id=data['room_id'])
    if request.user == question.user:
        return JsonResponse({'is_author':True})
    return JsonResponse({'is_author':False})
        



