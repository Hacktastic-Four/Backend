from django.urls import path
from .views import *
urlpatterns = [
    path("add-question/",add_question,name="add_question"),
    path("add-answer/",add_answer,name="add_answer"),
    path("upvote-answer/",upvote_answer,name="upvote_answer"),
    path("downvote-answer/",downvote_answer,name="downvote_answer"),
    path("get-all-questions/",get_all_questions,name="get_all_questions"),
    path("get-skills-questions/",get_skills_questions,name="get_skills_questions"),
    path("get-room-id/",get_room_id,name="get_room_id"),
]
