from django.db import models
from users.models import *

# Create your models here.
class Question(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    question = models.TextField(blank=True, null=True)
    topic = models.TextField(blank=True, null=True)
    room_id = models.UUIDField(blank=True,null=True)
    open = models.BooleanField(default=True)
    description = models.TextField(blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True,null=True)

    def __str__(self) -> str:
        return f"{self.user.email} - {self.id}"

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    answer = models.TextField(blank=True,null=True)
    video_link = models.TextField(blank=True,null=True)
    is_official = models.BooleanField(default=False)

    upvote = models.ManyToManyField(CustomUser, related_name='upvote',blank=True)
    downvote = models.ManyToManyField(CustomUser, related_name='downvote',blank=True)

    def __str__(self) -> str:
        return f"{self.question.id} - {self.id} - {self.user.email}"
    
    def upvote_count(self):
        return self.upvote.count()
    
    def downvote_count(self):
        return self.downvote.count()
