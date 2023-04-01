from django.urls import path
from .views import *
urlpatterns = [
    path("add-question/",add_question,name="add_question"),
    path("get-room-id/",get_room_id,name="get_room_id"),
]
